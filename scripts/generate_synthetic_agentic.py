"""
Sinh dữ liệu agentic synthetic (tuỳ chọn) — dùng OpenAI/Anthropic API.
Chạy: python scripts/generate_synthetic_agentic.py --n 200 --out data/agentic_synthetic.jsonl
"""
import os, json, argparse, random

TEMPLATES = [
    ("Tóm tắt {n} email và tạo báo cáo Excel", ["đọc_email","summarize","xuat_excel"]),
    ("Phân tích file CSV {n} dòng và vẽ biểu đồ", ["read_csv","pandas_analyze","plot_chart"]),
    ("Crawl {n} trang web và tổng hợp nội dung", ["http_get","html_parse","summarize"]),
    ("Giao {n} task song song: {tasks}", ["parallel_execute","aggregate"]),
]

def gen_one(i):
    t, tools = random.choice(TEMPLATES)
    n = random.choice([5, 10, 50, 100, 500])
    tasks = ", ".join(random.sample(["email","report","sheet","crawl","summary","translate"], 3))
    user = t.format(n=n, tasks=tasks)
    plan = "1) Phân tích task\n2) Chia nhỏ bước\n3) Gọi tool: " + ", ".join(tools) + "\n4) Tổng hợp và báo cáo."
    return {
        "text": f"<|im_start|>user\n{user}<|im_end|>\n<|im_start|>assistant\n{plan}<|im_end|>"
    }

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--out", default="data/agentic_synthetic.jsonl")
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        for i in range(args.n):
            f.write(json.dumps(gen_one(i), ensure_ascii=False) + "\n")
    print(f"✓ Sinh {args.n} mẫu → {args.out}")