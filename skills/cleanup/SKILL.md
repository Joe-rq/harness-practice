# Skill: cleanup

> 代码库清洁技能 - 对抗熵增的定期维护

## 触发条件

```yaml
trigger:
  events:
    - "scheduled"     # 定时触发
    - "manual"        # 手动触发
  schedule:
    frequency: "weekly"
    day: "sunday"
    time: "02:00"
  conditions:
    - "repository_exists"
```

## 清洁任务

### 1. 文档一致性检查

```python
# .harness/tasks/doc_consistency.py
"""
检查 docs/ 目录与实际代码的一致性
"""

class DocConsistencyChecker:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.docs_path = f"{repo_path}/docs"
        self.src_path = f"{repo_path}/src"
        
    def check(self):
        issues = []
        
        # 1.1 检查孤立的文档（没有对应的代码）
        orphan_docs = self.find_orphan_docs()
        issues.extend(orphan_docs)
        
        # 1.2 检查过时的 API 文档
        outdated = self.find_outdated_docs()
        issues.extend(outdated)
        
        # 1.3 检查缺失的文档（重要的公共接口没有文档）
        missing = self.find_missing_docs()
        issues.extend(missing)
        
        return issues
    
    def auto_fix(self, issues):
        """自动修复或生成 PR"""
        pr_body = self.generate_pr(issues)
        # 创建自动修复 PR
```

### 2. 架构违规扫描

```python
# .harness/tasks/arch_violation.py
"""
扫描架构约束违规
"""

class ArchitectureViolationScanner:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.rules = load_rules(".harness/lint-rules")
        
    def scan(self):
        violations = []
        
        # 2.1 扫描新增的违规导入
        import_violations = self.check_imports()
        violations.extend(import_violations)
        
        # 2.2 扫描命名退化
        naming_violations = self.check_naming()
        violations.extend(naming_violations)
        
        # 2.3 扫描复杂度退化
        complexity_violations = self.check_complexity()
        violations.extend(complexity_violations)
        
        return violations
```

### 3. 重复代码检测

```python
# .harness/tasks/duplicate_pattern.py
"""
检测代码库中的重复模式
"""

class DuplicatePatternDetector:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        
    def find_duplicates(self):
        # 使用 AST 分析检测重复代码
        # 阈值：连续 5 行以上相同
        
        duplicates = []
        
        for file in self.get_source_files():
            funcs = extract_functions(file)
            for i, func1 in enumerate(funcs):
                for func2 in funcs[i+1:]:
                    similarity = calculate_similarity(func1, func2)
                    if similarity > 0.8:
                        duplicates.append({
                            "file1": func1.path,
                            "file2": func2.path,
                            "similarity": similarity,
                            "suggestion": "抽取为公共函数"
                        })
        
        return duplicates
```

### 4. 死代码清理

```python
# .harness/tasks/dead_code.py
"""
清理未使用的代码
"""

class DeadCodeCleaner:
    def find_unused(self):
        unused = []
        
        # 4.1 未使用的函数
        unused_funcs = self.find_unused_functions()
        unused.extend(unused_funcs)
        
        # 4.2 未使用的导入
        unused_imports = self.find_unused_imports()
        unused.extend(unused_imports)
        
        # 4.3 未使用的变量
        unused_vars = self.find_unused_variables()
        unused.extend(unused_vars)
        
        return unused
```

## 执行流程

```
┌─────────────────────────────────────────────────────────┐
│                   Cleanup Agent                          │
├─────────────────────────────────────────────────────────┤
│  1. Doc Consistency    ──┐                             │
│  2. Arch Violation      ──┼──→ 聚合结果                 │
│  3. Duplicate Pattern   ──┤   ↓                        │
│  4. Dead Code          ──┘   ↓                        │
│                                        ↓               │
│  ┌─────────────────────────────────────────────────┐    │
│  │            生成修复建议/PR                       │    │
│  │  - 分类：auto-fix / need-review               │    │
│  │  - 优先级：critical / warning / info         │    │
│  └─────────────────────────────────────────────────┘    │
│                         ↓                               │
│  ┌─────────────────────────────────────────────────┐    │
│  │  CI 验证通过 → 自动合并                         │    │
│  │  CI 验证失败 → 标记需要人工介入                 │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## 输出格式

```yaml
cleanup_report:
  timestamp: "2026-03-17T10:00:00Z"
  duration_seconds: 180
  
  tasks:
    - name: "doc-consistency"
      status: "completed"
      issues_found: 5
      auto_fixed: 3
      need_review: 2
      
    - name: "arch-violation"
      status: "completed"
      issues_found: 2
      auto_fixed: 2
      need_review: 0
      
    - name: "duplicate-pattern"
      status: "completed"
      issues_found: 3
      auto_fixed: 0
      need_review: 3
      
    - name: "dead-code"
      status: "completed"
      issues_found: 8
      auto_fixed: 8
      need_review: 0
      
  summary:
    total_issues: 18
    auto_fixed: 13
    need_review: 5
    pr_created: true
    pr_url: "https://github.com/..."
```

## 配置

```yaml
skill:
  name: "cleanup"
  version: "1.0"
  
  config:
    schedule:
      frequency: "weekly"
      day: "sunday"
      time: "02:00"
      
    autoFix:
      enabled: true
      requireCI: true
      maxChangesPerPR: 20
      
    thresholds:
      duplicateSimilarity: 0.8
      minFunctionLines: 5
      complexityWarning: 15
      
    exclusions:
      - "*.test.ts"
      - "*.spec.ts"
      - "docs/"
```

## GitHub Actions 集成

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
      
      - name: Run Cleanup Agent
        run: |
          python -m .harness.tasks.cleanup --auto-fix
          
      - name: Create PR
        if: env.CHANGES == 'true'
        run: |
          gh pr create --title "Cleanup: $(date +%Y-%m-%d)" \
            --body-file .harness/templates/cleanup-pr.md
```
