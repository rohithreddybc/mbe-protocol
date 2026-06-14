#!/usr/bin/env python3
"""
MBE seed run: multiple KV-compression FAMILIES compared at matched budgets.

Faithful, self-contained implementations of:
  - full       : baseline (no compression)
  - kivi-4bit  : KIVI-style quantization (per-channel keys, per-token values; keeps all tokens)
  - streaming  : StreamingLLM (attention sinks + recent window) eviction
  - h2o        : Heavy-Hitter Oracle (keep highest accumulated-attention tokens + sinks + recent)

Eviction keeps a subset of cached (k, v); each kept key retains its prefill RoPE
rotation, and decode passes explicit true position_ids, so relative positions stay
correct. Task: synthetic passkey retrieval. Reports accuracy at the budget ladder.

This runs on CPU with a 0.5B model as a real, verifiable seed. The SAME code runs on
a 7-8B model on GPU (set MBE_MODEL and a CUDA device) to produce the paper-scale table.
"""
import json, os, sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.cache_utils import DynamicCache

MODEL = os.environ.get("MBE_MODEL", "Qwen/Qwen2.5-0.5B-Instruct")
N = int(os.environ.get("MBE_N", "8"))
BUDGETS = [0.25, 0.125]
SINK = 4
LOAD_4BIT = os.environ.get("MBE_LOAD_4BIT", "0") == "1"   # set 1 to fit 7-8B on a 16GB GPU
SKIP_H2O = os.environ.get("MBE_SKIP_H2O", "0") == "1"     # H2O needs output_attentions (memory)
USER_METHOD = os.environ.get("MBE_USER_METHOD")          # path to a .py exposing
#   def compress(legacy_cache, seqlen, budget, attn_importance) -> legacy_cache
#   (legacy_cache is a tuple of (key, value) per layer; quantize/evict and return it).
USER_NAME = os.environ.get("MBE_USER_NAME", "user-method")


def _load_user_compress():
    import importlib.util
    spec = importlib.util.spec_from_file_location("user_method", USER_METHOD)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.compress
USE_CUDA = torch.cuda.is_available()
DEVICE = "cuda" if USE_CUDA else "cpu"
torch.manual_seed(0)


def load_model_tok():
    tok = AutoTokenizer.from_pretrained(MODEL)
    kwargs = dict(attn_implementation="eager")
    if LOAD_4BIT:
        from transformers import BitsAndBytesConfig
        kwargs["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16, bnb_4bit_quant_type="nf4")
        kwargs["device_map"] = "auto"
    else:
        kwargs["dtype"] = torch.float16 if USE_CUDA else torch.float32
    model = AutoModelForCausalLM.from_pretrained(MODEL, **kwargs)
    if not LOAD_4BIT and USE_CUDA:
        model = model.to("cuda")
    model.eval()
    return model, tok


def make_sample(i, n_fillers=45):
    key = 1000 + 137 * (i + 1) % 9000
    fillers = " ".join(["The grass is green and the sky is blue."] * n_fillers)
    pos = len(fillers) // 2
    ctx = fillers[:pos] + f" The secret passkey is {key}. Remember it. " + fillers[pos:]
    msg = [{"role": "user", "content": ctx + "\n\nWhat is the secret passkey? Answer with the number only."}]
    return key, msg


def to_legacy(pkv):
    """List of (key, value) tensors per layer, robust across transformers 4.x and 5.x.
    (4.x exposes Cache.to_legacy_cache(); 5.x removed it and keeps key_cache/value_cache
    lists or a .layers list.)"""
    if pkv is None:
        return []
    if hasattr(pkv, "to_legacy_cache"):
        try:
            return list(pkv.to_legacy_cache())
        except Exception:
            pass
    if hasattr(pkv, "key_cache") and hasattr(pkv, "value_cache"):
        return [(k, v) for k, v in zip(pkv.key_cache, pkv.value_cache)]
    if hasattr(pkv, "layers"):
        return [(getattr(l, "keys", getattr(l, "key", None)),
                 getattr(l, "values", getattr(l, "value", None))) for l in pkv.layers]
    return list(pkv)


def from_legacy(legacy):
    """Build a cache the model can consume, robust across transformers 4.x and 5.x."""
    legacy = tuple(legacy)
    if hasattr(DynamicCache, "from_legacy_cache"):
        try:
            return DynamicCache.from_legacy_cache(legacy)
        except Exception:
            pass
    c = DynamicCache()
    for i, (k, v) in enumerate(legacy):
        c.update(k, v, i)
    return c


def quantize_cache(cache, bits=4, sink=4, recent=32):
    """KIVI-style fake-quant with a full-precision residual.

    Keys are quantized per channel (scale over the sequence), values per token.
    The first `sink` tokens (attention sink) and the last `recent` tokens are kept
    in full precision -- this is the standard KIVI residual and is essential at
    scale: large models place massive activations on the sink token, so quantizing
    it blows up the per-channel key scale and destroys 4-bit resolution for every
    other token (this is why a naive all-token quant returns ~0 on a 7-8B model
    while passing on a 0.5B one). Scales are computed in float32; a small epsilon
    underflows in fp16. The needle in the passkey task sits in the middle, so it is
    still quantized -- the residual fixes the outlier blow-up, it does not hide the
    needle behind a full-precision window."""
    qmax = 2 ** (bits - 1) - 1
    out = []
    for k, v in cache:
        seq = k.shape[2]
        lo = min(sink, seq)
        hi = max(lo, seq - recent)
        kq, vq = k.float().clone(), v.float().clone()
        if hi > lo:
            km = kq[:, :, lo:hi, :].clone()
            ks = km.abs().amax(dim=2, keepdim=True).clamp_min(1e-5) / qmax   # per channel
            kq[:, :, lo:hi, :] = torch.round(km / ks).clamp(-qmax - 1, qmax) * ks
            vm = vq[:, :, lo:hi, :].clone()
            vs = vm.abs().amax(dim=3, keepdim=True).clamp_min(1e-5) / qmax   # per token
            vq[:, :, lo:hi, :] = torch.round(vm / vs).clamp(-qmax - 1, qmax) * vs
        if os.environ.get("MBE_DEBUG") == "1" and len(out) == 0:
            bad = int(torch.isnan(kq).sum() + torch.isinf(kq).sum() +
                      torch.isnan(vq).sum() + torch.isinf(vq).sum())
            print(f"    [debug] layer0 seq={seq} keep=[{lo},{hi}) |k|max={k.abs().max().item():.3g} "
                  f"|v|max={v.abs().max().item():.3g} quant_nan_inf={bad}", flush=True)
        out.append((kq.to(k.dtype), vq.to(v.dtype)))
    return tuple(out)


def select_indices(method, seqlen, budget, attn_importance=None):
    keep = max(SINK + 1, int(round(budget * seqlen)))
    keep = min(keep, seqlen)
    sink = list(range(min(SINK, seqlen)))
    if method == "streaming":
        recent = keep - len(sink)
        idx = sink + list(range(seqlen - recent, seqlen))
    elif method == "h2o":
        recent_n = min(8, keep - len(sink))
        recent = list(range(seqlen - recent_n, seqlen))
        budget_left = keep - len(sink) - len(recent)
        forbidden = set(sink) | set(recent)
        cand = [(attn_importance[t].item(), t) for t in range(seqlen) if t not in forbidden]
        cand.sort(reverse=True)
        heavy = [t for _, t in cand[:max(0, budget_left)]]
        idx = sink + heavy + recent
    else:
        idx = list(range(seqlen))
    idx = sorted(set(i for i in idx if 0 <= i < seqlen))
    return torch.tensor(idx, dtype=torch.long)


def evict_cache(cache, idx):
    return tuple((k.index_select(2, idx), v.index_select(2, idx)) for k, v in cache)


@torch.no_grad()
def run(model, tok, method, budget, user_compress=None):
    correct = 0
    need_attn = method in ("h2o", "user")
    for i in range(N):
        key, msg = make_sample(i)
        ids = tok.apply_chat_template(msg, add_generation_prompt=True, return_tensors="pt")
        ids = ids.to(model.device)
        seqlen = ids.shape[1]
        out = model(ids, use_cache=True, output_attentions=need_attn)
        legacy = list(to_legacy(out.past_key_values))

        if method == "kivi-4bit":
            legacy = list(quantize_cache(legacy, 4))
        elif method == "user":
            imp = torch.zeros(seqlen)
            for a in out.attentions:
                imp += a[0].sum(dim=(0, 1))[:seqlen].float().cpu()
            legacy = list(user_compress(tuple(legacy), seqlen, budget, imp))
        elif method in ("streaming", "h2o"):
            imp = None
            if need_attn:
                # token importance = attention received, summed over layers/heads/queries
                imp = torch.zeros(seqlen)
                for a in out.attentions:            # a: [b, heads, q, kv]
                    imp += a[0].sum(dim=(0, 1))[:seqlen].float().cpu()
            idx = select_indices(method, seqlen, budget, imp).to(model.device)
            legacy = list(evict_cache(legacy, idx))

        cache = from_legacy(legacy)
        next_id = out.logits[:, -1].argmax(-1, keepdim=True)
        gen = [next_id.item()]
        pos = seqlen                                 # TRUE position of first generated token
        for _ in range(8):
            o = model(next_id, past_key_values=cache, use_cache=True,
                      position_ids=torch.tensor([[pos]], device=model.device))
            cache = o.past_key_values
            next_id = o.logits[:, -1].argmax(-1, keepdim=True)
            gen.append(next_id.item()); pos += 1
        ans = tok.decode(gen, skip_special_tokens=True)
        if str(key) in ans:
            correct += 1
    return correct / N


def main():
    print(f"Loading {MODEL}  (device={DEVICE}, 4bit={LOAD_4BIT}) ...", flush=True)
    model, tok = load_model_tok()
    user_compress = _load_user_compress() if USER_METHOD else None
    if USER_METHOD:
        methods = ["user"]                       # evaluate only the user's method (+ full baseline)
        print(f"Evaluating user method '{USER_NAME}' from {USER_METHOD}", flush=True)
    else:
        methods = ["kivi-4bit", "streaming"] + ([] if SKIP_H2O else ["h2o"])
    configs = [("full", None)]
    for m in methods:
        for b in BUDGETS:
            configs.append((m, b))

    rows = []
    for method, budget in configs:
        acc = run(model, tok, method, budget, user_compress)
        method_label = USER_NAME if method == "user" else method
        b = "100%" if budget is None else f"{int(budget*100*10)/10}%"
        print(f"  {method_label:14s} budget={b:6s} -> passkey acc {acc:.3f}", flush=True)
        rows.append({"method": method_label, "kv_budget": b, "passkey_acc": round(acc, 3)})

    safe_model = MODEL.split("/")[-1].lower()
    card = {
        "harness_version": "mbe-0.2.0",
        "run_type": ("GPU" if USE_CUDA else "CPU") + (" user-method run" if USER_METHOD else " seed run across families"),
        "model": MODEL,
        "task": "passkey retrieval (synthetic, single needle)",
        "n_samples": N,
        "hardware": (DEVICE + (" / 4-bit weights" if LOAD_4BIT else " / fp16" if USE_CUDA else " / float32")),
        "families": (USER_NAME if USER_METHOD else
                     "quantization (KIVI) + eviction (StreamingLLM sink+window, H2O heavy-hitter)"),
        "results": rows,
    }
    outdir = os.path.join(os.path.dirname(__file__), "..", "cards")
    os.makedirs(outdir, exist_ok=True)
    tag = (USER_NAME.replace(" ", "-").replace("/", "-") if USER_METHOD else "seed_multimethod")
    out = os.path.join(outdir, f"{tag}_{safe_model}.json")
    json.dump(card, open(out, "w"), indent=2)
    print("Wrote", out, flush=True)


if __name__ == "__main__":
    main()
