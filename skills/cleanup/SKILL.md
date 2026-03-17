---
name: cleanup
description: |
  代码库清洁技能 - 对抗代码库熵增的定期维护。
  触发场景：(1) 每周定时 (2) 手动触发 (3) CI 失败后修复
---

# Cleanup Skill

## 快速开始

```bash
# 完整清洁
python scripts/cleanup.py

# 仅检查（不自动修复）
python scripts/cleanup.py --check-only

# 指定任务
python scripts/cleanup.py --task doc-consistency
python scripts/cleanup.py --task arch-violation
python scripts/cleanup.py --task duplicate-pattern

# 自动修复
python scripts/cleanup.py --auto-fix
```

## 清洁任务

### 1. 文档一致性
- 检查孤立文档（无对应代码）
- 检查过时 API 文档
- 检查缺失文档

### 2. 架构违规
- 扫描违规导入
- 扫描命名退化
- 扫描复杂度退化

### 3. 重复代码
- 检测重复函数
- 建议抽取为公共函数

### 4. 死代码
- 未使用函数
- 未使用导入
- 未使用变量

## 定时任务配置

详见 [references/schedule.md](references/schedule.md)
