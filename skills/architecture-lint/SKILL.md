# Skill: architecture-lint

> 架构约束检查技能 - 把"品味"编码成机器可执行的检查

## 触发条件

```yaml
trigger:
  events:
    - "pre_commit"
    - "ci_pipeline"
  conditions:
    - "always"
```

## 检查规则

### 1. 层级依赖检查

```python
# .harness/lint-rules/check_layer_dependency.py
"""
层级依赖规则：
UI → Runtime → Service → Repo → Config → Types

任何层只能向下依赖，不能向上依赖
"""

RULES = {
    "UI": ["Runtime", "Service", "Repo", "Config", "Types"],
    "Runtime": ["Service", "Repo", "Config", "Types"],
    "Service": ["Repo", "Config", "Types"],
    "Repo": ["Config", "Types"],
    "Config": ["Types"],
    "Types": []
}

def check_layer_dependency(file_path, import_list):
    """检查导入是否违反层级依赖"""
    current_layer = detect_layer(file_path)
    allowed_layers = RULES.get(current_layer, [])
    
    for imp in import_list:
        imp_layer = detect_layer(imp)
        if imp_layer not in allowed_layers:
            return Violation(
                file=file_path,
                rule="layer_dependency",
                message=f"{current_layer} cannot import {imp_layer}"
            )
```

### 2. 命名规范检查

```python
# .harness/lint-rules/check_naming.py
"""
命名规范：
- 类名：PascalCase (e.g., UserService)
- 函数/变量：snake_case (e.g., get_user)
- 常量：UPPER_SNAKE_CASE (e.g., MAX_RETRIES)
- 文件名：kebab-case (e.g., user-service.py)
"""

NAMING_RULES = {
    "class": r"^[A-Z][a-zA-Z0-9]*$",
    "function": r"^[a-z_][a-z0-9_]*$",
    "constant": r"^[A-Z][A-Z0-9_]*$",
    "file": r"^[a-z0-9-]+\.[a-z]+$"
}
```

### 3. 循环依赖检查

```python
# .harness/lint-rules/check_circular_deps.py
"""
检测模块间的循环依赖
"""

def find_circular_deps(module_graph):
    """使用 DFS 检测循环"""
    visited = set()
    path = []
    
    def dfs(node):
        if node in path:
            return True
        if node in visited:
            return False
            
        path.append(node)
        for dep in module_graph.get(node, []):
            if dfs(dep):
                return True
        path.pop()
        visited.add(node)
        return False
        
    return dfs
```

### 4. 复杂度检查

```python
# .harness/lint-rules/check_complexity.py
"""
圈复杂度检查：
- 函数最大复杂度: 10
- 类最大复杂度: 20
- 文件最大行数: 500
"""

COMPLEXITY_THRESHOLDS = {
    "function": 10,
    "class": 20,
    "file": 500
}
```

## 执行方式

### 本地 pre-commit hook
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: architecture-lint
        name: Harness Architecture Lint
        entry: python .harness/lint-rules/run_all.py
        language: system
        pass_filenames: false
        types: [python, typescript, javascript]
        stages: [pre-commit]
```

### CI 检查
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
          python .harness/lint-rules/run_all.py --strict
```

## 输出格式

```yaml
lint_result:
  passed: boolean
  
  violations:
    - file: "src/ui/user_view.py"
      line: 42
      rule: "layer_dependency"
      message: "UI cannot import Types directly"
      severity: "error"
      suggestion: "Move import to Service layer"
      
  metrics:
    totalFiles: number
    totalViolations: number
    errors: number
    warnings: number
```

## 错误信息示例

```
❌ layer_dependency (error)
   src/ui/user_view.py:42
   UI cannot import Types (UserModel)
   → 建议：通过 Service 层间接访问

❌ naming (warning)
   src/service/userService.py:10
   文件名应为 kebab-case
   → 建议：重命名为 user-service.py

❌ complexity (warning)
   src/service/complex_service.py:100
   函数复杂度 15 > 阈值 10
   → 建议：拆分为多个小函数
```

## 配置

```yaml
skill:
  name: "architecture-lint"
  version: "1.0"
  
  config:
    strictMode: true
    failOnError: true
    failOnWarning: false
    
  rules:
    - layer_dependency
    - naming
    - circular_deps
    - complexity
    - file_length
    - test_coverage
```
