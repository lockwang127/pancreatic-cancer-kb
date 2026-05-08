#!/usr/bin/env python3
"""
知识库格式验证测试
验证所有知识三元组是否符合Schema规范
"""

import json
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

KB_DIR = Path(__file__).parent.parent.parent / "data" / "knowledge-graph"
SCHEMA_FILE = Path(__file__).parent.parent.parent / "schemas" / "triplet_schema.json"

# 必需字段
REQUIRED_FIELDS = ["head", "relation", "tail"]
# 可选字段
OPTIONAL_FIELDS = ["source", "evidence", "domain", "confidence", "pmid"]
# 有效枚举值
VALID_SOURCES = ["指南", "文献", "临床试验", "专家共识", "数据库"]
VALID_DOMAINS = ["流行病学", "诊断", "分期", "治疗", "预后", "生物标志物", "病理"]


def load_schema():
    """加载Schema定义"""
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_triplet(triplet, file_name, index):
    """验证单个三元组"""
    errors = []

    # 检查必需字段
    for field in REQUIRED_FIELDS:
        if field not in triplet:
            errors.append(f"  [{file_name}:{index}] 缺少必需字段 '{field}'")
        elif not triplet[field] or str(triplet[field]).strip() == "":
            errors.append(f"  [{file_name}:{index}] 字段 '{field}' 为空")

    # 检查confidence范围
    if "confidence" in triplet:
        conf = triplet["confidence"]
        if not isinstance(conf, (int, float)):
            errors.append(f"  [{file_name}:{index}] confidence应为数字")
        elif conf < 0 or conf > 1:
            errors.append(f"  [{file_name}:{index}] confidence超出0-1范围: {conf}")

    # 检查source枚举
    if "source" in triplet and triplet["source"] not in VALID_SOURCES:
        errors.append(f"  [{file_name}:{index}] source值无效: {triplet['source']}")

    # 检查domain枚举
    if "domain" in triplet and triplet["domain"] not in VALID_DOMAINS:
        errors.append(f"  [{file_name}:{index}] domain值无效: {triplet['domain']}")

    return errors


def validate_knowledge_file(file_path):
    """验证单个知识文件"""
    errors = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"[{file_path.name}] JSON格式错误: {e}"]

    # 检查顶层结构
    if "knowledge_triplets" not in data:
        return [f"[{file_path.name}] 缺少 'knowledge_triplets' 字段"]

    triplets = data["knowledge_triplets"]
    if not isinstance(triplets, list):
        return [f"[{file_path.name}] 'knowledge_triplets' 应为数组"]

    if len(triplets) == 0:
        return [f"[{file_path.name}] 'knowledge_triplets' 为空"]

    # 验证每个三元组
    for i, triplet in enumerate(triplets):
        if not isinstance(triplet, dict):
            errors.append(f"  [{file_path.name}:{i}] 三元组应为对象")
            continue
        errors.extend(validate_triplet(triplet, file_path.name, i))

    return errors


def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("知识库格式验证测试")
    print("=" * 60)

    # 加载Schema
    schema = load_schema()
    print(f"\n加载Schema: {SCHEMA_FILE.name}")

    # 查找知识文件
    kb_files = list(KB_DIR.glob("*.json"))
    knowledge_files = [f for f in kb_files if f.name not in ["kb.json", "kb_meta.json"]]

    print(f"\n发现 {len(knowledge_files)} 个知识文件待验证")

    all_errors = []
    total_triplets = 0

    for kb_file in knowledge_files:
        print(f"\n验证: {kb_file.name}")
        errors = validate_knowledge_file(kb_file)

        # 统计三元组数量
        with open(kb_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        count = len(data.get("knowledge_triplets", []))
        total_triplets += count

        if errors:
            print(f"  ✗ 发现 {len(errors)} 个错误")
            all_errors.extend(errors)
        else:
            print(f"  ✓ 通过 ({count} 条三元组)")

    # 输出结果
    print("\n" + "=" * 60)
    print("测试结果")
    print("=" * 60)

    if all_errors:
        print(f"\n✗ 验证失败，发现 {len(all_errors)} 个错误:")
        for error in all_errors[:50]:  # 最多显示50个错误
            print(error)
        if len(all_errors) > 50:
            print(f"  ... 还有 {len(all_errors) - 50} 个错误")
        return False
    else:
        print(f"\n✓ 所有验证通过!")
        print(f"  - 知识文件数: {len(knowledge_files)}")
        print(f"  - 总三元组数: {total_triplets}")
        return True


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
