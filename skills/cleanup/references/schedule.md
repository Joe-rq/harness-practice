# Cleanup 定时任务配置

## GitHub Actions

```yaml
# .github/workflows/cleanup.yml
name: Weekly Cleanup
on:
  schedule:
    - cron: '0 2 * * 0'  # 每周日 02:00
  workflow_dispatch:

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install vulture
      
      - name: Run Cleanup
        run: |
          python skills/cleanup/scripts/cleanup.py --check-only
      
      - name: Create PR
        if: failure()
        run: |
          gh pr create --title "Cleanup: $(date +%Y-%m-%d)" \
            --body "自动生成的清洁任务"
```

## 任务说明

| 任务 | 频率 | 说明 |
|------|------|------|
| doc-consistency | weekly | 文档与代码一致性 |
| arch-violation | daily | 架构违规扫描 |
| duplicate-pattern | weekly | 重复代码检测 |
| dead-code | daily | 死代码清理 |

## 自动修复流程

```
1. 运行 cleanup.py --check-only
2. 聚合问题列表
3. 生成修复建议
4. 创建 PR
5. CI 验证
6. 自动合并（可选）
```

## 阈值配置

```yaml
# cleanup.yaml
thresholds:
  duplicateSimilarity: 0.8    # 重复代码相似度
  minFunctionLines: 5         # 最小函数行数
  complexityWarning: 15      # 复杂度警告阈值
  
autoFix:
  enabled: true
  requireCI: true
  maxChangesPerPR: 20
```
