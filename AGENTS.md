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
├── AGENTS.md                 # ← 入口：目录地图
├── .claude/
│   ├── config.json           # MCP 配置
│   └── settings.json         # Claude Code 设置
├── .harness/
│   ├── config.yaml           # Harness 全局配置
│   ├── lint-rules/           # Linter 规则
│   ├── context/              # 动态上下文
│   └── prompts/              # 提示词模板
├── docs/                    # 知识库
│   ├── architecture/         # 架构文档
│   ├── domains/              # 业务域文档
│   ├── plans/                # 执行计划
│   ├── specs/                # 产品规格
│   └── runbooks/             # 操作手册
├── skills/                   # Skill 定义
│   ├── code-review/
│   │   └── SKILL.md
│   ├── architecture-lint/
│   │   └── SKILL.md
│   └── cleanup/
│       └── SKILL.md
└── src/                     # 业务代码
```

## 核心概念

### 1. AGENTS.md 当地图
AGENTS.md 不是百科全书，而是"目录地图"。告诉 Agent：
- 项目结构是怎样的
- 关键文档在哪
- 遇到问题找谁/找什么

### 2. 约束换自主
- 规矩越明确 → Agent 独立做的事越多
- Linter 规则必须强制执行
- Review 流程必须闭环

### 3. 进度追踪
每个复杂任务创建 `.harness/progress/` 下的追踪文件：
```yaml
# .harness/progress/{task-id}.yaml
task: "功能名称"
status: "in_progress"  # pending / in_progress / done / failed
completed_steps:
  - "步骤1"
  - "步骤2"
next_step: "步骤3"
blockers: []
```

## 常用命令

```bash
# 运行架构检查
make lint

# 运行测试
make test

# 触发清洁 Agent
make clean

# 生成进度报告
make report
```

## Skill 参考

### code-review
- 触发：文件变更 > 100 行
- 执行：安全扫描 → 架构合规 → 测试覆盖

### architecture-lint
- 触发：每次提交
- 执行：层级依赖检查 → 命名规范 → 安全检查

### cleanup
- 触发：每周定时
- 执行：文档一致性 → 架构违规 → 重复模式

## 文档

- [Harness 配置](.harness/config.yaml)
- [Linter 规则](.harness/lint-rules/README.md)
- [Skill 定义](skills/)
