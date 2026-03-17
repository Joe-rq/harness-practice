# Harness Practice - AI Agent 控制系统

> 本项目是 Harness Engineering 实践的本地实现，基于 Claude Code 运行。

## 快速开始

### 前提条件
- Claude Code (`npm install -g @anthropic-ai/claude-code`)
- Node.js 18+
- Python 3.10+

### 安装
```bash
# 克隆项目
git clone https://github.com/Joe-rq/harness-practice.git
cd harness-practice

# 安装依赖
pip install -r examples/drg-helper/requirements.txt
pip install vulture black flake8 pre-commit

# 安装 pre-commit hooks
pre-commit install

# 启动 Claude Code
claude
```

## 项目结构

```
.
├── AGENTS.md                      # ← 入口：目录地图
├── .claude/
│   └── config.json                # ← MCP 配置（含6个工具）
├── .harness/
│   ├── config.yaml               # Harness 全局配置
│   ├── progress/                 # 任务进度追踪
│   └── data.db                  # SQLite 数据存储
├── .github/workflows/
│   └── harness-ci.yml           # ← CI 配置
├── .pre-commit-config.yaml       # ← pre-commit 配置
├── skills/                       # ← Skill 定义
│   ├── code-review/
│   ├── architecture-lint/
│   └── cleanup/
├── examples/                      # ← 示例项目
│   ├── run-demo.sh
│   └── drg-helper/
├── docs/                         # ← 知识库
│   ├── medical/                  # 医疗领域知识
│   ├── IMPLEMENTATION_STATUS.md # 对标分析
│   └── WORKFLOW_EXAMPLE.md     # 工作流示例
└── src/                         # 业务代码
```

## 新增功能

### ✅ CI/CD 集成
- GitHub Actions 自动运行 lint + test + cleanup
- pre-commit hook 本地检查

### ✅ MCP 工具扩展
- 文件系统（读写）
- 浏览器自动化
- SQLite 数据库
- Git 操作
- 代码搜索

### ✅ 知识库
- 医疗健康领域知识（ICD-10, ICD-9-CM-3, DRG）
- 工作流示例（完整任务流程）

## 使用流程

### 1. 本地开发
```bash
# 编写代码
vim src/models/drg.py

# pre-commit 自动检查
git add .
git commit  # 自动触发 lint + review
```

### 2. 代码审查
```bash
python skills/code-review/scripts/run_review.py --files src/
```

### 3. 架构检查
```bash
python skills/architecture-lint/scripts/run_all.py --strict
```

### 4. 运行测试
```bash
cd examples/drg-helper
python -m pytest tests/ -v
```

### 5. 清理检查
```bash
python skills/cleanup/scripts/cleanup.py --check-only
```

## 文档

- [Harness 配置](.harness/config.yaml)
- [MCP 配置](.claude/config.json)
- [CI 配置](.github/workflows/harness-ci.yml)
- [Pre-commit 配置](.pre-commit-config.yaml)
- [实现对标](docs/IMPLEMENTATION_STATUS.md)
- [工作流示例](docs/WORKFLOW_EXAMPLE.md)
- [医疗知识库](docs/medical/README.md)
