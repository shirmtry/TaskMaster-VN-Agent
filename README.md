# TaskMaster-VN-Agent

SLM tiếng Việt agentic — fine-tune QLoRA trên nền Qwen2.5.
Chạy được trên CPU để test toàn bộ pipeline trước khi train thật trên GPU.
Demo Gradio CPU-friendly, không cần GPU.

## Cấu trúc repo

```
TaskMaster-VN-Agent/
├── .gitignore
├── README.md
├── requirements.txt
├── app.py
├── configs/
│   └── train_config.yaml
├── data/
│   └── .gitkeep
├── models/
│   └── .gitkeep
├── notebooks/
│   └── train_slm_4060.ipynb
└── scripts/
    ├── push_repo.py
    └── generate_synthetic_agentic.py
```

## Cài đặt

```bash
git clone https://github.com/shirmtry/TaskMaster-VN-Agent.git
cd TaskMaster-VN-Agent
pip install -r requirements.txt
```

## Chạy notebook (CPU test)

```bash
jupyter notebook notebooks/train_slm_4060.ipynb
# CPU_MODE = True mặc định → test toàn bộ pipeline, không cần GPU
```

## Chạy demo

```bash
python app.py
# Mở http://localhost:7860
```

## Khi có GPU (RTX 4060 32GB)

```
1. Mở notebook, đổi CPU_MODE = False
2. Set os.environ["HF_TOKEN"] để push model lên Hugging Face
3. Chạy Cell 5 → 7 để train thật + export GGUF
4. Cập nhật app.py để dùng model mới
```

## Dataset sử dụng

- `VietnamAIHub/General_Domain_Vietnamese_Instructions_V1`
- `glaiveai/glaive-function-calling-v2`
- `II-Vietnam/Agentic-Search-MultiHop` (fallback an toàn)

Nếu không tải được dataset nào (gated/private/offline), notebook tự sinh 20 mẫu giả lập để vẫn test được pipeline.

## License

MIT

![Python](https://img.shields.io/badge/python-3.10%2B-blue)