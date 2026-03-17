#!/bin/bash
# DRG Helper - Harness 流程演示

set -e

echo "========================================"
echo "DRG Helper - Harness 流程演示"
echo "========================================"

# 1. 代码审查
echo ""
echo "Step 1: 运行代码审查..."
echo "---------------------------------------"
python skills/code-review/scripts/run_review.py --files "examples/drg-helper/src/" --mode full

# 2. 架构检查
echo ""
echo "Step 2: 运行架构检查..."
echo "---------------------------------------"
python skills/architecture-lint/scripts/run_all.py --strict || true

# 3. 运行测试
echo ""
echo "Step 3: 运行测试..."
echo "---------------------------------------"
cd examples/drg-helper
pip install -q -r requirements.txt
python -m pytest tests/ -v

# 4. 清理检查
echo ""
echo "Step 4: 运行清理检查..."
echo "---------------------------------------"
python skills/cleanup/scripts/cleanup.py --check-only

echo ""
echo "========================================"
echo "演示完成!"
echo "========================================"
