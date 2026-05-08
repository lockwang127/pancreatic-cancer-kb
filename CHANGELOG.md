# 更新日志 (CHANGELOG)

所有知识库的重要更新都会记录在此。

## [1.0.0] - 2026-05-08

### 初始版本

#### 新增
- **流行病学知识域**: 13条三元组
  - 中国2022年发病/死亡数据
  - 5年生存率、危险因素
  - 病理类型分布

- **分期与生物标志物**: 15条三元组
  - AJCC第8版TNM分期
  - 可切除性评估标准
  - CA19-9等标志物

- **CSCO 2024指南**: 15条三元组
  - 可切除癌辅助化疗方案
  - 边界可切除新辅助治疗
  - 晚期一线FOLFIRINOX方案
  - BRCA突变PARP抑制剂

- **治疗方案**: 15条三元组
  - 手术方式（Whipple术、胰体尾切除）
  - 化疗方案详细剂量
  - 靶向/维持治疗

#### 构建
- `data/kb.json`: 完整知识库 (58条三元组)
- `data/kb_meta.json`: 元数据

#### 脚本
- `scripts/build_kb.py`: 知识库构建
- `scripts/sync_to_github.py`: GitHub同步
- `scripts/tests/test_kb_format.py`: 格式验证

#### 文档
- README.md
- UPDATE_POLICY.md
- DEPLOY.md
- docs/domain_guide.md

---

格式规范:
- [版本号] - 日期
- ### 新增/修改/修复
- #### 具体条目
