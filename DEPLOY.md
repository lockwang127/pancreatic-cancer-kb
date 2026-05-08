# 部署指南 (DEPLOY)

本指南帮助您将胰腺癌知识库部署到GitHub。

## 前置要求

- Git已安装
- GitHub账号
- SSH密钥已配置（用于Git操作）

## 部署步骤

### 1. 创建GitHub仓库

1. 访问 [GitHub New Repository](https://github.com/new)
2. 配置仓库信息:
   - **Repository name**: `pancreatic-cancer-kb`
   - **Description**: `基于结构化知识三元组的胰腺癌医学知识库`
   - - **Privacy**: 选择 `Public`（公开仓库）
   - **Initialize**: 不要勾选任何初始化选项

### 2. 连接本地仓库到GitHub

在 `pancreatic-cancer-kb` 目录下执行:

```bash
# 添加远程仓库
git remote add origin git@github.com:lockwang127/pancreatic-cancer-kb.git

# 重命名主分支为main
git branch -M main

# 推送代码到GitHub
git push -u origin main
```

### 3. 验证部署

推送成功后，访问:
```
https://github.com/lockwang127/pancreatic-cancer-kb
```

应能看到完整的仓库内容。

## 后续更新

### 提交更改

```bash
git add .
git commit -m "Your commit message"
git push
```

### 重建知识库

修改知识文件后:

```bash
# 运行格式验证
python3 scripts/tests/test_kb_format.py

# 重建知识库
python3 scripts/build_kb.py

# 提交并推送
git add .
git commit -m "build: 重建知识库"
git push
```

## 目录说明

```
pancreatic-cancer-kb/
├── data/
│   ├── kb.json        # 生成的完整知识库
│   └── kb_meta.json    # 生成的元数据
├── .gitignore         # 已配置忽略 __pycache__
└── (其他文件)
```

## 故障排除

### SSH连接问题

```bash
# 测试SSH连接
ssh -T git@github.com

# 如果失败，检查SSH密钥
ssh-keygen -t ed25519 -C "your_email@example.com"
# 添加到GitHub Settings > SSH Keys
```

### 远程仓库已存在

如果 `git remote add` 报错远程已存在:

```bash
# 查看当前远程
git remote -v

# 如果URL错误，更新它
git remote set-url origin git@github.com:lockwang127/pancreatic-cancer-kb.git
```

## 自动化（可选）

### 使用GitHub Actions自动构建

在仓库根目录创建 `.github/workflows/build.yml`:

```yaml
name: Build Knowledge Base

on:
  push:
    branches: [main]
    paths:
      - 'data/knowledge-graph/**/*.json'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Build KB
        run: python3 scripts/build_kb.py
      - name: Validate
        run: python3 scripts/tests/test_kb_format.py
```

## 联系方式

如有问题，请提交 [GitHub Issue](https://github.com/lockwang127/pancreatic-cancer-kb/issues)
