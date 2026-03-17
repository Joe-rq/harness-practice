# Harness Practice - AI Agent 控制系统

> 本项目是 Harness Engineering 实践的本地实现，基于 Claude Code 运行。

## 快速开始

### 前提条件
- Claude Code (`npm install -g @anthropic-ai/claude-code`)
- Node.js 18+
- Python 3.10+

### 启动
```bash
# 安装依赖
npm install

# 启动 Claude Code
claude
```

## 项目结构

```
.
├── AGENTS.md                      # ← 入口：目录地图
├── .claude/
│   └── config.json                # MCP 配置
├── .harness/
│   ├── config.yaml               # Harness 全局配置
│   └── progress/                 # 任务进度追踪
├── skills/                        # ← Skill 定义（符合 AgentSkills 规范）
│   ├── code-review/
│   ├── architecture-lint/
│   └── cleanup/
├── examples/                      # ← 示例项目
│   ├── run-demo.sh              # 演示脚本
│   └── drg-helper/              # DRG 分组助手示例
└── docs/                         # 知识库
```

## 核心概念

### 1. Skill 结构（AgentSkills 规范）
每个 Skill 包含：
- `SKILL.md` - 入口文件（YAML frontmatter + 简洁说明）
- `scripts/` - 可执行代码
- `references/` - 参考资料（按需加载）

### 2. 约束换自主
- 规矩越明确 → Agent 独立做的事越多
- Linter 规则必须强制执行
- Review 流程必须闭环

### 3. 进度追踪
每个复杂任务创建 `.harness/progress/` 下的追踪文件。

## 示例项目

### DRG Helper - 诊断相关分组助手

一个展示完整 Harness 工程流程的示例项目。

**功能**：根据患者诊断和手术信息自动计算 DRG 分组

**技术栈**：Python + FastAPI + SQLite

**目录结构**：
```
examples/drg-helper/
├── src/
│   ├── api/main.py              # FastAPI 服务
│   └── models/drg.py            # DRG 分组逻辑
├── tests/
│   └── test_drg.py              # 单元测试
├── docs/
│   └── drg-rules.md             # DRG 规则文档
└── requirements.txt
```

**运行演示**：
```bash
# 方式1: 一键演示
bash examples/run-demo.sh

# 方式2: 逐步执行
cd examples/drg-helper
pip install -r requirements.txt

# 代码审查
python ../../skills/code-review/scripts/run_review.py --files src/ --mode full

# 架构检查
python ../../skills/architecture-lint/scripts/run_all.py --strict

# 运行测试
python -m pytest tests/ -v
```

## Skills

### code-review
代码审查技能
```bash
python skills/code-review/scripts/run_review.py --files src/main.py
```

### architecture-lint
架构约束检查
```bash
python skills/architecture-lint/scripts/run_all.py --strict
```

### cleanup
代码库清洁
```bash
python skills/cleanup/scripts/cleanup.py --auto-fix
```

## 文档

- [Harness 配置](.harness/config.yaml)
- [Code Review Skill](skills/code-review/SKILL.md)
- [Architecture Lint Skill](skills/architecture-lint/SKILL.md)
- [Cleanup Skill](skills/cleanup/SKILL.md)
- [DRG 规则文档](examples/drg-helper/docs/drg-rules.md)
