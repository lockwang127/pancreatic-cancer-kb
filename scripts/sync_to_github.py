#!/usr/bin/env python3
"""
GitHub同步脚本
将本地知识库推送到GitHub远程仓库
"""

import os
import subprocess
from pathlib import Path


def check_git_status():
    """检查Git状态"""
    repo_dir = Path(__file__).parent.parent

    # 检查是否为Git仓库
    if not (repo_dir / ".git").exists():
        print("错误: 当前目录不是Git仓库")
        print("请先运行: git init")
        return False

    # 检查远程仓库配置
    result = subprocess.run(
        ["git", "remote", "-v"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )

    if "origin" not in result.stdout:
        print("警告: 未配置远程仓库(origin)")
        print("\n请按以下步骤操作:")
        print("1. 访问 https://github.com/new 创建名为 'pancreatic-cancer-kb' 的仓库（选择Public）")
        print("2. 运行命令:")
        print("   git remote add origin git@github.com:lockwang127/pancreatic-cancer-kb.git")
        print("   git branch -M main")
        print("   git push -u origin main")
        return False

    return True


def sync_to_github():
    """同步到GitHub"""
    repo_dir = Path(__file__).parent.parent

    print("=" * 60)
    print("GitHub同步检查")
    print("=" * 60)

    if not check_git_status():
        print("\n同步中止。请先完成Git远程仓库配置。")
        return

    # 获取当前分支状态
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )

    if result.stdout.strip():
        print("\n有未提交的更改:")
        print(result.stdout)

        # 检查是否有build生成的文件
        kb_file = repo_dir / "data" / "kb.json"
        meta_file = repo_dir / "data" / "kb_meta.json"

        if kb_file.exists():
            print(f"\n发现生成的 kb.json ({(kb_file.stat().st_size / 1024):.1f} KB)")
        if meta_file.exists():
            print(f"发现生成的 kb_meta.json")

        print("\n请运行以下命令提交并推送:")
        print("  git add .")
        print("  git commit -m 'Your commit message'")
        print("  git push -u origin main")

    else:
        print("\n没有未提交的更改，工作区干净。")

    # 检查远程分支
    result = subprocess.run(
        ["git", "remote", "-v"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    print(f"\n远程仓库配置:")
    print(result.stdout)

    print("\n" + "=" * 60)
    print("检查完成!")
    print("=" * 60)


if __name__ == "__main__":
    sync_to_github()
