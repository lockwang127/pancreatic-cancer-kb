#!/usr/bin/env python3
"""
胰腺癌知识库构建脚本
将分散的知识图谱文件整合为统一的kb.json和kb_meta.json
"""

import json
import os
from pathlib import Path
from datetime import datetime

KB_DIR = Path(__file__).parent.parent / "data" / "knowledge-graph"
OUTPUT_DIR = Path(__file__).parent.parent / "data"


def load_knowledge_files():
    """加载所有知识图谱文件"""
    kb_files = list(KB_DIR.glob("*.json"))
    all_triplets = []
    metadata = {
        "files": [],
        "domains": set(),
        "total_triplets": 0
    }

    for kb_file in kb_files:
        if kb_file.name in ["kb.json", "kb_meta.json"]:
            continue

        with open(kb_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        triplets = data.get("knowledge_triplets", [])
        all_triplets.extend(triplets)

        # 收集元数据
        file_domains = set(t["domain"] for t in triplets if "domain" in t)
        metadata["files"].append({
            "name": kb_file.name,
            "triplet_count": len(triplets),
            "domains": list(file_domains)
        })
        metadata["domains"].update(file_domains)

    metadata["total_triplets"] = len(all_triplets)
    metadata["total_domains"] = len(metadata["domains"])

    return all_triplets, metadata


def build_kb():
    """构建知识库主函数"""
    print("=" * 60)
    print("胰腺癌知识库构建")
    print("=" * 60)

    # 检查知识文件
    kb_files = list(KB_DIR.glob("*.json"))
    knowledge_files = [f for f in kb_files if f.name not in ["kb.json", "kb_meta.json"]]

    print(f"\n发现 {len(knowledge_files)} 个知识文件:")
    for f in knowledge_files:
        print(f"  - {f.name}")

    # 加载知识
    triplets, metadata = load_knowledge_files()

    print(f"\n知识统计:")
    print(f"  - 总三元组数: {metadata['total_triplets']}")
    print(f"  - 知识领域数: {metadata['total_domains']}")
    print(f"  - 领域列表: {', '.join(metadata['domains'])}")

    # 生成kb.json
    kb_data = {
        "version": "1.0.0",
        "name": "胰腺癌知识库",
        "description": "基于CSCO指南和相关文献的结构化胰腺癌知识图谱",
        "built_at": datetime.now().isoformat(),
        "knowledge_graph": triplets
    }

    kb_path = OUTPUT_DIR / "kb.json"
    with open(kb_path, "w", encoding="utf-8") as f:
        json.dump(kb_data, f, ensure_ascii=False, indent=2)
    print(f"\n生成文件: {kb_path}")

    # 生成kb_meta.json
    meta_data = {
        "version": "1.0.0",
        "name": "胰腺癌知识库元数据",
        "built_at": datetime.now().isoformat(),
        "total_triplets": metadata["total_triplets"],
        "total_domains": metadata["total_domains"],
        "domains": list(metadata["domains"]),
        "source_files": metadata["files"]
    }

    meta_path = OUTPUT_DIR / "kb_meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_data, f, ensure_ascii=False, indent=2)
    print(f"生成文件: {meta_path}")

    print("\n" + "=" * 60)
    print("构建完成!")
    print("=" * 60)

    return metadata["total_triplets"], metadata["total_domains"]


if __name__ == "__main__":
    build_kb()
