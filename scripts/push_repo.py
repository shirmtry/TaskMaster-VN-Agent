"""
Script tạo repo GitHub và push toàn bộ code lên.
Cách dùng:
    export GITHUB_TOKEN=ghp_xxx
    python scripts/push_repo.py
"""
import os, sys, subprocess, shutil
from pathlib import Path

TOKEN = os.environ.get("GITHUB_TOKEN")
if not TOKEN:
    sys.exit("Thiếu GITHUB_TOKEN. Set biến môi trường rồi chạy lại.")

REPO_NAME = os.environ.get("REPO_NAME", "TaskMaster-VN-Agent")
PRIVATE = os.environ.get("REPO_PRIVATE", "false").lower() == "true"

# Di chuyển lên thư mục gốc repo (cha của scripts/)
ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
print(f"Working dir: {ROOT}")

from github import Github, Auth
g = Github(auth=Auth.Token(TOKEN))
user = g.get_user()
print(f"GitHub user: {user.login}")

# Tạo repo nếu chưa có
try:
    repo = user.get_repo(REPO_NAME)
    print(f"Repo đã tồn tại: {repo.html_url}")
except Exception:
    repo = user.create_repo(REPO_NAME, private=PRIVATE, description="SLM Vietnamese Agentic - CPU testable")
    print(f"Đã tạo repo mới: {repo.html_url}")

# Git init + push
def sh(cmd, check=True):
    # Che token trong log để tránh lộ credential
    safe = cmd.replace(TOKEN, "***")
    print(f"$ {safe[:100]}")
    return subprocess.run(cmd, shell=True, check=check)

# Xóa .git cũ nếu có (đảm bảo fresh) — dùng shutil để chạy được cả Windows
if (ROOT / ".git").exists():
    shutil.rmtree(ROOT / ".git", ignore_errors=True)

sh("git init -b main")
sh("git add .")
sh('git -c user.email="bot@local" -c user.name="TaskMaster Bot" '
   'commit -m "init: notebook CPU + demo + scripts"')
sh(f"git remote add origin https://{TOKEN}@github.com/{user.login}/{REPO_NAME}.git")
sh("git push -u origin main -f")

print(f"\n✅ Xong: {repo.html_url}")