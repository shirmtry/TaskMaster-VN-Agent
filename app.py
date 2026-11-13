"""
TaskMaster-VN Demo — chạy được trên CPU, không cần GPU.
Mặc định dùng Qwen2.5-0.5B GGUF (~400MB) tải từ HF Hub khi khởi động.
Nếu không tải được → fallback rule-based để UI vẫn chạy.
"""
import os, gradio as gr

DEMO_REPO = os.environ.get("DEMO_MODEL_REPO", "Qwen/Qwen2.5-0.5B-Instruct-GGUF")
DEMO_FILE = os.environ.get("DEMO_MODEL_FILE", "qwen2.5-0.5b-instruct-q4_k_m.gguf")

llm = None
mode = "rule_based"
try:
    from huggingface_hub import hf_hub_download
    from llama_cpp import Llama
    path = hf_hub_download(repo_id=DEMO_REPO, filename=DEMO_FILE)
    llm = Llama(model_path=path, n_ctx=2048, n_threads=max(1, os.cpu_count()//2), verbose=False)
    mode = "llm"
    print(f"[OK] Đã load {DEMO_FILE}")
except Exception as e:
    print(f"[WARN] Không load được model ({e}). Dùng fallback rule-based.")

def chat_fn(message, history):
    if mode == "rule_based" or llm is None:
        return (f"[DEMO MODE - rule-based]\n"
                f"Task nhận: {message}\n\n"
                f"TaskMaster-VN (mô phỏng):\n"
                f"1) Phân tích task\n"
                f"2) Chia nhỏ bước\n"
                f"3) Gọi tool (file/email/db/...)\n"
                f"4) Tổng hợp báo cáo\n\n"
                f"(Model thật sẽ chạy sau khi train xong trên GPU.)")
    prompt = f"<|im_start|>user\n{message}<|im_end|>\n<|im_start|>assistant\n"
    out = llm(prompt, max_tokens=256, stop=["<|im_end|>"], echo=False)
    return out["choices"][0]["text"].strip()

with gr.Blocks(title="TaskMaster-VN Demo") as demo:
    gr.Markdown("# TaskMaster-VN-Agent Demo\n**SLM tiếng Việt agentic — chạy CPU**\n\nDemo dùng Qwen2.5-0.5B. Model 7B fine-tune sẽ có sau khi train trên RTX 4060.")
    gr.ChatInterface(
        fn=chat_fn,
        examples=[
            "Tóm tắt 50 email và tạo báo cáo Excel",
            "Phân tích file CSV 10.000 dòng và vẽ biểu đồ",
            "Giao 5 task song song: gửi mail, tạo báo cáo, update sheet, crawl web, tổng hợp",
        ],
    )
    gr.Markdown(f"**Chế độ:** `{mode}")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)