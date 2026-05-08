# 胰腺癌知识库 (Pancreatic Cancer Knowledge Base)

基于结构化知识三元组的胰腺癌医学知识库，支持RAG/LLM应用集成。

## 概述

本知识库收录胰腺癌流行病学、诊断、分期、治疗等领域的结构化知识，基于CSCO 2024指南和相关文献构建。

## 仓库结构

```
pancreatic-cancer-kb/
├── data/
│   ├── knowledge-graph/       # 知识图谱源文件
│   │   ├── epidemiology.json  # 流行病学数据
│   │   ├── biomarkers.json    # 分期与生物标志物
│   │   ├── csco_2024.json     # CSCO指南推荐
│   │   └── treatment.json     # 治疗方案
│   ├── kb.json               # 构建后的完整知识库
│   └── kb_meta.json           # 知识库元数据
├── scripts/
│   ├── build_kb.py            # 知识库构建脚本
│   ├── sync_to_github.py      # GitHub同步检查
│   └── tests/
│       └── test_kb_format.py  # 格式验证测试
├── schemas/
│   └── triplet_schema.json    # 知识三元组Schema
├── docs/
│   └── domain_guide.md        # 领域指南
├── README.md
├── UPDATE_POLICY.md
├── CHANGELOG.md
└── DEPLOY.md
```

## 知识三元组格式

每个知识条目采用 `head-relation-tail` 三元组结构：

```json
{
  "head": "胰腺癌",
  "relation": "5年生存率",
  "tail": "约12%",
  "source": "文献",
  "evidence": "全球常见恶性肿瘤中最低之一",
  "domain": "流行病学",
  "confidence": 0.95
}
```

### 字段说明

| 字段 | 必需 | 说明 |
|------|------|------|
| head | 是 | 实体头节点/主语 |
| relation | 是 | 关系类型 |
| tail | 是 | 实体尾节点/宾语 |
| source | 否 | 证据来源（指南/文献/临床试验/专家共识/数据库） |
| evidence | 否 | 具体证据描述 |
| domain | 否 | 知识领域 |
| confidence | 否 | 置信度 0-1 |
| pmid | 否 | PubMed ID |

## 知识领域

- **流行病学**: 发病率、死亡率、危险因素
- **诊断**: 影像学、实验室检查
- **分期**: TNM分期、可切除性评估
- **生物标志物**: CA19-9、CEA等
- **治疗**: 手术、化疗、放疗、靶向治疗

## 快速开始

### 构建知识库

```bash
cd pancreatic-cancer-kb
python3 scripts/build_kb.py
```

### 验证格式

```bash
python3 scripts/tests/test_kb_format.py
```

### 同步到GitHub

详见 [DEPLOY.md](DEPLOY.md)

## 使用方式

### Python调用

```python
import json

with open("data/kb.json", "r", encoding="utf-8") as f:
    kb = json.load(f)

for triplet in kb["knowledge_graph"]:
    print(f"{triplet['head']} - {triplet['relation']} - {triplet['tail']}")
```

### RAG应用集成

```python
# 检索相关知识
def search_knowledge(kb, domain=None, keyword=None):
    results = kb["knowledge_graph"]
    if domain:
        results = [t for t in results if t.get("domain") == domain]
    if keyword:
        results = [t for t in results if keyword in t["head"] or keyword in t["tail"]]
    return results
```

## 数据来源

- CSCO胰腺癌诊疗指南 2024
- NCCN Guidelines Pancreatic Cancer
- AJCC Cancer Staging Manual 第8版
- GLOBOCAN 2022
- PubMed相关文献

## 贡献指南

详见 [UPDATE_POLICY.md](UPDATE_POLICY.md)

## License

MIT License

## 维护者

lockwang127
