# 知识库更新策略 (UPDATE_POLICY)

## 版本管理

### 版本号格式
- 主版本.次版本.修订号 (e.g., 1.0.0)
- 主版本: 重大结构变更
- 次版本: 新增知识域或大规模知识更新
- 修订号: 小幅修正、补充、格式调整

### 变更记录
所有更新必须在 [CHANGELOG.md](CHANGELOG.md) 中记录。

## 知识添加规范

### 新增三元组要求

1. **准确性**: 必须有明确文献/指南来源
2. **完整性**: 必须包含所有必需字段
3. **格式**: 符合 `schemas/triplet_schema.json` 规范

### 必需字段
```json
{
  "head": "实体名称",
  "relation": "关系描述",
  "tail": "实体值/对象"
}
```

### 推荐字段
```json
{
  "source": "指南|文献|临床试验|专家共识|数据库",
  "evidence": "具体证据描述",
  "domain": "流行病学|诊断|分期|治疗|预后|生物标志物|病理",
  "confidence": 0.0-1.0,
  "pmid": "PubMed ID"
}
```

## 质量标准

### 知识质量分级

| 级别 | confidence | 说明 |
|------|------------|------|
| A级 | 0.95-1.0 | 指南/专家共识明确推荐 |
| B级 | 0.85-0.94 | 高质量文献支持 |
| C级 | 0.70-0.84 | 一般文献/专家经验 |
| D级 | <0.70 | 探索性/初步研究 |

### 来源优先级

1. CSCO/NCCN指南（最高优先级）
2. 大型随机对照试验（RCT）
3. 系统综述/Meta分析
4. 专家共识
5. 一般文献

## 更新流程

### 1. 本地修改
```bash
# 创建新分支
git checkout -b update/new-knowledge

# 编辑知识文件
vim data/knowledge-graph/xxx.json

# 运行格式验证
python3 scripts/tests/test_kb_format.py

# 提交更改
git add .
git commit -m "docs: 添加XXX知识三元组"
```

### 2. 构建知识库
```bash
python3 scripts/build_kb.py
git add data/kb.json data/kb_meta.json
git commit -m "build: 重建知识库"
```

### 3. 推送更新
```bash
git push origin update/new-knowledge
# 创建Pull Request
```

## 知识审核

### 自动审核
- JSON格式验证
- 必需字段检查
- 枚举值校验
- confidence范围检查

### 人工审核
- 新增知识域需审核
- 大规模更新需审核
- 涉及临床决策的关键信息需审核

## 知识撤回

如发现错误知识：
1. 在CHANGELOG中记录撤回原因
2. 修改/删除错误三元组
3. 重新构建知识库
4. 提交变更

## 联系方式

问题反馈: GitHub Issues
