#!/usr/bin/env python3
"""
MBE proof-of-concept run (CPU). FAITHFUL KV-cache quantization on a real 0.5B model
(Qwen2.5-0.5B-Instruct, GQA) over a passkey-retrieval task, at matched bit-budgets.

This is a SMOKE TEST, not the paper's 7-8B result: small model, small N, CPU. It
exists to (a) prove the harness runs end-to-end and (b) produce *real* numbers under
matched budgets. Methods: full FP, then per-channel-key / per-token-value symmetric
quantization of the prefill KV cache at 8 / 4 / 2 bits (KIVI-style).
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
N = int(os.environ.get("MBE_N", "12"))
torch.manual_seed(0)


def make_sample(i, n_fillers=40):
    key = 1000 + 137 * (i + 1) % 9000          # deterministic 4-digit passkey
    fillers = " ".join(
        ["The grass is green and the sky is blue."] * n_fillers)
    pos = len(fillers) // 2
    ctx = (fillers[:pos] +
           f" The secret passkey is {key}. Remember it. " + fillers[pos:])
    msg = [{"role": "user",
            "content": ctx + f"\n\nWhat is the secret passkey? Answer with the number only."}]
    return key, msg


def quantize_cache(cache, bits):
    """Symmetric KIVI-style quant-dequant of a legacy cache tuple.
    keys: per-channel (over seq); values: per-token (over head_dim)."""
    qmax = 2 ** (bits - 1) - 1
    out = []
    for k, v in cache:
        # k,v: [b, n_kv_heads, seq, head_dim]; compute in fp32 (1e-8 underflows in fp16)
        kf, vf = k.float(), v.float()
        ks = kf.abs().amax(dim=2, keepdim=True).clamp_min(1e-5) / qmax     # per-channel
        kq = torch.round(kf / ks).clamp(-qmax - 1, qmax) * ks
        vs = vf.abs().amax(dim=3, keepdim=True).clamp_min(1e-5) / qmax     # per-token
        vq = torch.round(vf / vs).clamp(-qmax - 1, qmax) * vs
        out.append((kq.to(k.dtype), vq.to(v.dtype)))
    return tuple(out)


@torch.no_grad()
def run_method(model, tok, bits):
    correct = 0
    for i in range(N):
        key, msg = make_sample(i)
        ids = tok.apply_chat_template(msg, add_generation_prompt=True,
                                      return_tensors="pt")
        # prefill
        out = model(ids, use_cache=True)
        past = out.past_key_values
        legacy = past.to_legacy_cache() if hasattr(past, "to_legacy_cache") else past
        if bits is not None:
            legacy = quantize_cache(legacy, bits)
        cache = DynamicCache.from_legacy_cache(legacy)
        # greedy decode
        next_id = out.logits[:, -1].argmax(-1, keepdim=True)
        gen = [next_id.item()]
        cur = ids
        for _ in range(8):
            o = model(next_id, past_key_values=cache, use_cache=True)
            cache = o.past_key_values
            next_id = o.logits[:, -1].argmax(-1, keepdim=True)
            gen.append(next_id.item())
        ans = tok.decode(gen, skip_special_tokens=True)
        if str(key) in ans:
            correct += 1
        safe = ans.strip()[:20].encode("ascii", "replace").decode("ascii")
        print(f"  bits={bits}  sample {i+1}/{N}  key={key}  got='{safe}'  {'OK' if str(key) in ans else 'x'}",
              flush=True)
    return correct / N


def main():
    print(f"Loading {MODEL} on CPU ...", flush=True)
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.float32)
    model.eval()
    cfg = model.config
    print(f"layers={cfg.num_hidden_layers} kv_heads={getattr(cfg,'num_key_value_heads','?')} "
          f"q_heads={cfg.num_attention_heads}", flush=True)

    results = {}
    for label, bits in [("full-FP", None), ("KV-8bit", 8), ("KV-4bit", 4), ("KV-2bit", 2)]:
        print(f"[{label}]", flush=True)
        acc = run_method(model, tok, bits)
        budget = "100%" if bits is None else f"{bits/16*100:.1f}%"
        results[label] = {"kv_budget": budget, "passkey_acc": round(acc, 3)}
        print(f"  -> passkey accuracy = {acc:.3f}\n", flush=True)

    card = {
        "harness_version": "mbe-0.1.0",
        "run_type": "CPU smoke test (proof-of-concept, NOT the 7-8B suite)",
        "model": MODEL,
        "model_size": "0.5B (GQA)",
        "task": "passkey retrieval (synthetic, single needle)",
        "n_samples": N,
        "hardware": "CPU / float32",
        "method_family": "KV quantization (KIVI-style: per-channel keys, per-token values)",
        "results": results,
    }
    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "cards"), exist_ok=True)
    out = os.path.join(os.path.dirname(__file__), "..", "cards",
                       "smoke_quant_qwen2.5-0.5b.json")
    with open(out, "w") as f:
        json.dump(card, f, indent=2)
    print("Wrote", out)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
