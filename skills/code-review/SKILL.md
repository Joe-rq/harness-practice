# Skill: code-review

> AI Agent 代码审查技能，基于 Claude Code + MCP

## 触发条件

```yaml
trigger:
  events:
    - "file_changed"
    - "pr_created"
  conditions:
    - "lines_changed > 100"
    - "file_type in [py, ts, js, go, rs]"
```

## 审查流程

### Step 1: 安全扫描
```bash
# 1.1 扫描硬编码密钥
grep -r "password\|api_key\|secret\|token" --include="*.py" --include="*.ts"

# 1.2 扫描 SQL 注入风险
grep -r "execute\|query\|raw" --include="*.py" | grep -v "parametrized"

# 1.3 扫描 XSS 风险
grep -r "innerHTML\|dangerouslySetInnerHTML" --include="*.ts" --include="*.js"
```

### Step 2: 架构合规
```bash
# 2.1 检查层级依赖
python .harness/lint-rules/check_layer_dependency.py

# 2.2 检查命名规范
python .harness/lint-rules/check_naming.py

# 2.3 检查循环依赖
python .harness/lint-rules/check_circular_deps.py
```

### Step 3: 测试覆盖
```bash
# 3.1 检查测试存在性
ls -la tests/

# 3.2 运行测试
make test

# 3.3 生成覆盖率报告
make coverage
```

### Step 4: 代码质量
```bash
# 4.1 运行 linter
make lint

# 4.2 检查复杂度
python .harness/lint-rules/check_complexity.py

# 4.3 检查重复代码
python .harness/lint-rules/check_duplicates.py
```

## 输出格式

```yaml
review_result:
  decision: "approve" | "request_changes" | "reject"
  
  findings:
    - severity: "critical" | "warning" | "info"
      category: "security" | "architecture" | "testing" | "quality"
      location: "file:line"
      description: "问题描述"
      suggestion: "修复建议"
      
  metrics:
    linesAdded: number
    linesRemoved: number
    testCoverage: number
    complexity: number
    
  summary: "总结"
```

## 配置

```yaml
skill:
  name: "code-review"
  version: "1.0"
  
  config:
    minReviewApproval: 1
    autoApproveThreshold: "low"
    requireTests: true
    requireDocumentation: false
    
  modes:
    - name: "fast"
      timeout: 60
      checks: ["security", "syntax"]
      
    - name: "full"
      timeout: 300
      checks: ["security", "architecture", "testing", "quality"]
```

## 示例

```bash
# 手动触发审查
claude /skill code-review --files src/main.py

# 查看审查结果
cat .harness/reviews/$(date +%Y%m%d)-main.py.md
```
