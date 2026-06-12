"""
MBE Leaderboard — a Hugging Face Space (Gradio) that renders submitted
KV Compression Cards from the MBE dataset as a sortable leaderboard.

Deploy: create a Space (SDK: gradio), push this folder. It pulls cards live from
the dataset repo so the board updates as cards are submitted.
"""
import json
import gradio as gr
from huggingface_hub import HfApi, hf_hub_download

DATASET = "Rohithreddybc/kv-cache-compression-mbe"


def load_rows():
    api = HfApi()
    rows = []
    try:
        files = [f for f in api.list_repo_files(DATASET, repo_type="dataset")
                 if f.startswith("cards/") and f.endswith(".json")]
    except Exception as e:
        return [["(could not reach dataset)", str(e), "", "", ""]]
    for f in files:
        try:
            p = hf_hub_download(DATASET, f, repo_type="dataset")
            card = json.load(open(p))
            model = card.get("model", "?")
            run_type = card.get("run_type", "")
            results = card.get("results", {})
            # results may be a dict {method: {...}} or a list of {method, kv_budget, passkey_acc}
            items = results.values() if isinstance(results, dict) else results
            for r in items:
                rows.append([
                    card.get("families", card.get("method_family", "")),
                    r.get("method", "") if isinstance(r, dict) else "",
                    r.get("kv_budget", ""),
                    r.get("passkey_acc", r.get("accuracy", "")),
                    model,
                ])
        except Exception:
            continue
    return rows or [["(no cards yet)", "", "", "", ""]]


with gr.Blocks(title="KV Cache Compression Leaderboard (MBE)") as demo:
    gr.Markdown(
        "# KV Cache Compression Leaderboard — Matched-Budget Evaluation (MBE)\n"
        "Matched-Budget Evaluation: methods compared at fixed KV-memory budgets. "
        "Cards are pulled live from "
        "[`Rohithreddybc/kv-cache-compression-mbe`](https://huggingface.co/datasets/Rohithreddybc/kv-cache-compression-mbe). "
        "Submit your own via the [GitHub repo](https://github.com/rohithreddybc/mbe-protocol). "
        "**Compare within a (model, budget) group only.**")
    table = gr.Dataframe(
        headers=["Family", "Method", "KV budget", "Accuracy / retention", "Model"],
        datatype=["str", "str", "str", "str", "str"], interactive=False, wrap=True)
    btn = gr.Button("Refresh")
    demo.load(load_rows, outputs=table)
    btn.click(load_rows, outputs=table)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
