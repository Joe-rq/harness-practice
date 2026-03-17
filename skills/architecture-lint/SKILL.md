---
name: architecture-lint
description: |
  架构约束检查技能 - 把"品味"编码成机器可执行的检查。
  触发场景：(1) pre-commit hook (2) CI pipeline (3) 手动运行
---

# Architecture Lint Skill

## 快速开始

```bash
# 运行全部检查
python scripts/run_all.py

# 运行特定检查
python scripts/run_all.py --rule layer_dependency
python scripts/scripts/run_all.py --rule naming
python scripts/run_all.py --rule complexity

# CI 模式（严格模式）
python scripts/run_all.py --strict
```

## 检查规则

### 1. 层级依赖
```
UI → Runtime → Service → Repo → Config → Types
```
任何层只能向下依赖。

### 2. 命名规范
- 类名: PascalCase
- 函数: snake_case
- 常量: UPPER_SNAKE_CASE
- 文件: kebab-case

### 3. 循环依赖
检测模块间循环依赖。

### 4. 复杂度
- 函数最大复杂度: 10
- 类最大复杂度: 20
- 文件最大行数: 500

## 配置

详见 [references/rules.md](references/rules.md)
