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
torch.manual_seed(0)


def make_sample(i, n_fillers=45):
    key = 1000 + 137 * (i + 1) % 9000
    fillers = " ".join(["The grass is green and the sky is blue."] * n_fillers)
    pos = len(fillers) // 2
    ctx = fillers[:pos] + f" The secret passkey is {key}. Remember it. " + fillers[pos:]
    msg = [{"role": "user", "content": ctx + "\n\nWhat is the secret passkey? Answer with the number only."}]
    return key, msg


def quantize_cache(cache, bits=4):
    qmax = 2 ** (bits - 1) - 1
    out = []
    for k, v in cache:
        ks = k.abs().amax(dim=2, keepdim=True).clamp_min(1e-8) / qmax
        kq = torch.round(k / ks).clamp(-qmax - 1, qmax) * ks
        vs = v.abs().amax(dim=3, keepdim=True).clamp_min(1e-8) / qmax
        vq = torch.round(v / vs).clamp(-qmax - 1, qmax) * vs
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
def run(model, tok, method, budget):
    correct = 0
    need_attn = (method == "h2o")
    for i in range(N):
        key, msg = make_sample(i)
        ids = tok.apply_chat_template(msg, add_generation_prompt=True, return_tensors="pt")
        seqlen = ids.shape[1]
        out = model(ids, use_cache=True, output_attentions=need_attn)
        legacy = list(out.past_key_values.to_legacy_cache())

        if method == "kivi-4bit":
            legacy = list(quantize_cache(legacy, 4))
        elif method in ("streaming", "h2o"):
            imp = None
            if need_attn:
                # token importance = attention received, summed over layers/heads/queries
                imp = torch.zeros(seqlen)
                for a in out.attentions:            # a: [b, heads, q, kv]
                    imp += a[0].sum(dim=(0, 1))[:seqlen].float()
            idx = select_indices(method, seqlen, budget, imp)
            legacy = list(evict_cache(legacy, idx))

        cache = DynamicCache.from_legacy_cache(tuple(legacy))
        next_id = out.logits[:, -1].argmax(-1, keepdim=True)
        gen = [next_id.item()]
        pos = seqlen                                 # TRUE position of first generated token
        for _ in range(8):
            o = model(next_id, past_key_values=cache, use_cache=True,
                      position_ids=torch.tensor([[pos]]))
            cache = o.past_key_values
            next_id = o.logits[:, -1].argmax(-1, keepdim=True)
            gen.append(next_id.item()); pos += 1
        ans = tok.decode(gen, skip_special_tokens=True)
        if str(key) in ans:
            correct += 1
    return correct / N


def main():
    print(f"Loading {MODEL} ...", flush=True)
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, torch_dtype=torch.float32, attn_implementation="eager")
    model.eval()

    configs = [("full", None)]
    for m in ["kivi-4bit", "streaming", "h2o"]:
        for b in BUDGETS:
            configs.append((m, b))

    rows = []
    for method, budget in configs:
        acc = run(model, tok, method, budget)
        b = "100%" if budget is None else f"{int(budget*100*10)/10}%"
        print(f"  {method:12s} budget={b:6s} -> passkey acc {acc:.3f}", flush=True)
        rows.append({"method": method, "kv_budget": b, "passkey_acc": round(acc, 3)})

    card = {
        "harness_version": "mbe-0.2.0",
        "run_type": "CPU seed run (proof-of-concept across families, NOT the 7-8B suite)",
        "model": MODEL, "model_size": "0.5B (GQA)",
        "task": "passkey retrieval (synthetic, single needle)",
        "n_samples": N, "hardware": "CPU / float32",
        "families": "quantization (KIVI) + eviction (StreamingLLM sink+window, H2O heavy-hitter)",
        "results": rows,
    }
    outdir = os.path.join(os.path.dirname(__file__), "..", "cards")
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "seed_multimethod_qwen2.5-0.5b.json")
    json.dump(card, open(out, "w"), indent=2)
    print("Wrote", out, flush=True)


if __name__ == "__main__":
    main()
