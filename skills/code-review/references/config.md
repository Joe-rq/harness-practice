# Code Review 配置参考

## 审查模式

### Fast 模式
- 超时: 60s
- 检查项: security, syntax

### Full 模式
- 超时: 300s
- 检查项: security, architecture, testing, quality

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

## 安全规则

| 规则 | 严重性 | 说明 |
|------|--------|------|
| hardcoded_secret | critical | 硬编码密钥 |
| sql_injection | critical | SQL 注入风险 |
| xss | critical | XSS 漏洞 |
| weak_crypto | warning | 弱加密算法 |

## 架构规则

| 规则 | 严重性 | 说明 |
|------|--------|------|
| layer_dependency | error | 层级依赖违规 |
| naming_convention | warning | 命名规范 |
| circular_dependency | error | 循环依赖 |
