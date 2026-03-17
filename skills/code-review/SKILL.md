---
name: code-review
description: |
  AI Agent 代码审查技能。用于对代码变更进行安全、架构、测试合规性检查。
  触发场景：(1) 文件变更 > 100 行 (2) PR 创建 (3) 手动触发审查
---

# Code Review Skill

## 快速开始

```bash
# 完整审查
python scripts/run_review.py --files src/main.py

# 快速审查（仅安全+语法）
python scripts/run_review.py --files src/main.py --mode fast

# 查看结果
cat .harness/reviews/latest.md
```

## 审查流程

### 1. 安全扫描
- 硬编码密钥检测
- SQL 注入风险
- XSS 漏洞检测

### 2. 架构合规
- 层级依赖检查
- 命名规范验证
- 循环依赖检测

### 3. 测试覆盖
- 测试文件存在性
- 测试执行
- 覆盖率报告

### 4. 代码质量
- Lint 检查
- 复杂度分析
- 重复代码检测

## 配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| mode | full | 审查模式：fast/full |
| minLines | 100 | 触发审查的最小变更行数 |
| requireTests | true | 是否要求测试 |

详见 [references/config.md](references/config.md)
