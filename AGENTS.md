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
│   │   ├── SKILL.md             # 入口
│   │   ├── scripts/             # 可执行脚本
│   │   └── references/          # 参考资料
│   ├── architecture-lint/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── references/
│   └── cleanup/
│       ├── SKILL.md
│       ├── scripts/
│       └── references/
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
