# Harness 任务工作流示例

> 展示如何使用 Harness 系统处理一个完整的开发任务

## 场景: 添加新的 DRG 分组规则

### 任务描述

在 DRG Helper 系统中添加"骨髓移植"相关分组规则。

---

## Step 1: 创建任务追踪

```yaml
# .harness/progress/bmt-grouping-feature.yaml
task: "添加骨髓移植 DRG 分组规则"
status: "in_progress"
description: "支持骨髓干细胞移植的 DRG 分组"
created_at: "2026-03-17T10:00:00Z"

files:
  - "src/models/drg.py"
  - "tests/test_drg.py"
  - "docs/drg-rules.md"

completed_steps:
  - "分析现有 DRG 分组逻辑"
  - "确定相关 MDC 和 ADRG"

next_step: "实现分组逻辑"

blockers: []

decisions: []
```

---

## Step 2: 代码审查 (Agent 互审)

```bash
# Agent A 提交代码变更后，触发 Agent B 审查
python skills/code-review/scripts/run_review.py \
  --files "src/models/drg.py" \
  --mode full
```

### 审查结果

```yaml
decision: "request_changes"

findings:
  - severity: "warning"
    category: "architecture"
    location: "src/models/drg.py:120"
    description: "函数长度超过 50 行"
    suggestion: "拆分为多个小函数"
    
  - severity: "info"
    category: "testing"
    location: "tests/test_drg.py"
    description: "缺少骨髓移植测试用例"
    suggestion: "添加 test_bone_marrow_transplant"

metrics:
  linesAdded: 45
  linesRemoved: 2
  testCoverage: 75%
```

---

## Step 3: 修复问题

### 3.1 拆分函数

```python
# 之前
def calculate(self, patient):
    # 100+ 行代码
    ...

# 之后
def calculate(self, patient):
    mdc = self._get_mdc(patient)
    adrg = self._get_adrg(mdc, patient)
    drg = self._get_drg(adrg, patient)
    return self._build_result(drg)
```

### 3.2 添加测试

```python
def test_bone_marrow_transplant(self):
    """测试骨髓移植分组"""
    patient = PatientInfo(
        patient_id="P100",
        age=35,
        gender="M",
        admission_type="elective",
        principal_diagnosis="C91.1",  # 急性淋巴细胞白血病
        secondary_diagnoses=["D70.0"],  # 粒细胞减少
        procedures=["41.00"]  # 骨髓移植
    )
    
    result = self.group.calculate(patient)
    
    assert result.mdc == "17"  # 血液疾病
    assert "移植" in result.description
```

---

## Step 4: 再次审查

```bash
python skills/code-review/scripts/run_review.py \
  --files "src/models/drg.py" \
  --mode full
```

### 审查结果

```yaml
decision: "approve"

findings: []

metrics:
  linesAdded: 30
  linesRemoved: 45
  testCoverage: 85%
```

---

## Step 5: 架构检查

```bash
python skills/architecture-lint/scripts/run_all.py --strict
```

### 检查结果

```
✅ 通过所有检查
  - 层级依赖: 通过
  - 命名规范: 通过
  - 复杂度: 通过
```

---

## Step 6: 提交代码

```bash
git add src/models/drg.py tests/test_drg.py docs/drg-rules.md
git commit -m "feat: 添加骨髓移植 DRG 分组规则

- 支持干细胞移植分组
- 添加相关测试用例
- 更新文档"
```

---

## Step 7: CI 验证

GitHub Actions 自动运行:

1. **Architecture Lint** ✅
2. **Run Tests** ✅ (8 passed)
3. **Cleanup Check** ⚠️ (1 warning: 文档过长)

---

## Step 8: 更新进度

```yaml
# .harness/progress/bmt-grouping-feature.yaml
task: "添加骨髓移植 DRG 分组规则"
status: "done"
completed_at: "2026-03-17T11:30:00Z"

completed_steps:
  - "分析现有 DRG 分组逻辑"
  - "确定相关 MDC 和 ADRG"
  - "实现分组逻辑"
  - "添加测试用例"
  - "通过代码审查"
  - "通过架构检查"
  - "CI 验证通过"
  - "合并代码"

verification:
  passed: true
  tests_run: 8
  issues: []
```

---

## 完整流程时间线

```
10:00 - 创建任务
10:05 - 第一次审查 → request_changes
10:15 - 修复问题
10:20 - 第二次审查 → approve
10:25 - 架构检查 → 通过
10:30 - 提交代码
10:35 - CI 验证 → 通过
11:30 - 合并代码 → 完成
```

---

## 关键洞察

1. **Agent 互审有效**: 第一次审查发现了架构问题，避免了技术债务
2. **自动化检查节省时间**: CI 自动运行 lint + test
3. **进度追踪清晰**: 每个步骤都有记录，便于回顾和审计
