# 架构规则详细说明

## 层级依赖规则

```
UI → Runtime → Service → Repo → Config → Types
```

| 层 | 可导入 |
|---|--------|
| UI | Runtime, Service, Repo, Config, Types |
| Runtime | Service, Repo, Config, Types |
| Service | Repo, Config, Types |
| Repo | Config, Types |
| Config | Types |
| Types | 无 |

## 复杂度阈值

| 类型 | 阈值 |
|------|------|
| 函数 | 10 (圈复杂度) |
| 类 | 20 (圈复杂度) |
| 文件 | 500 行 |
| 函数长度 | 50 行 |

## 命名规范

| 类型 | 规则 | 示例 |
|------|------|------|
| 类名 | PascalCase | UserService |
| 函数 | snake_case | get_user |
| 常量 | UPPER_SNAKE | MAX_RETRIES |
| 文件 | kebab-case | user-service.py |
| 数据库表 | snake_case | user_info |

## CI 配置

```yaml
# .github/workflows/arch-lint.yml
name: Architecture Lint
on: [pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Architecture Lint
        run: |
          python skills/architecture-lint/scripts/run_all.py --strict
```

## Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: architecture-lint
        name: Harness Architecture Lint
        entry: python skills/architecture-lint/scripts/run_all.py
        language: system
        types: [python, typescript]
        stages: [pre-commit]
```
