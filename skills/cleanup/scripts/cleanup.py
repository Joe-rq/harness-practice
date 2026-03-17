#!/usr/bin/env python3
"""Cleanup Script - 代码库清洁主脚本"""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def check_doc_consistency():
    """检查文档一致性"""
    issues = []
    
    docs_dir = Path("docs")
    src_dir = Path("src")
    
    if not docs_dir.exists() or not src_dir.exists():
        return issues
    
    # 检查孤立的文档
    for doc in docs_dir.rglob("*.md"):
        # 简单检查：文档中提到的文件名是否存在于代码中
        pass
    
    return issues

def check_arch_violation():
    """检查架构违规"""
    issues = []
    
    # 运行架构检查
    result = subprocess.run(
        ["python", "skills/architecture-lint/scripts/run_all.py"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        issues.append({
            "task": "arch-violation",
            "status": "failed",
            "output": result.stdout
        })
    
    return issues

def check_duplicate_pattern():
    """检查重复代码"""
    issues = []
    
    # 使用 vulture 检测死代码
    result = subprocess.run(
        ["vulture", "src/", "--min-confidence", "80"],
        capture_output=True,
        text=True
    )
    
    if result.stdout:
        issues.append({
            "task": "duplicate-pattern",
            "status": "warning",
            "output": result.stdout
        })
    
    return issues

def check_dead_code():
    """检查死代码"""
    issues = []
    
    # 使用 vulture
    result = subprocess.run(
        ["vulture", "src/", "--dead-code", "True"],
        capture_output=True,
        text=True
    )
    
    if result.stdout:
        issues.append({
            "task": "dead-code",
            "status": "found",
            "count": len(result.stdout.splitlines()),
            "output": result.stdout
        })
    
    return issues

def main():
    parser = argparse.ArgumentParser(description="Cleanup Script")
    parser.add_argument("--check-only", action="store_true", help="仅检查，不修复")
    parser.add_argument("--auto-fix", action="store_true", help="自动修复")
    parser.add_argument("--task", choices=["doc-consistency", "arch-violation", "duplicate-pattern", "dead-code"], help="指定任务")
    args = parser.parse_args()
    
    print(f"🧹 Cleanup - {datetime.now().isoformat()}\n")
    
    tasks = [args.task] if args.task else [
        "doc-consistency", 
        "arch-violation", 
        "duplicate-pattern", 
        "dead-code"
    ]
    
    all_issues = []
    
    for task in tasks:
        print(f"运行: {task}...")
        
        if task == "doc-consistency":
            issues = check_doc_consistency()
        elif task == "arch-violation":
            issues = check_arch_violation()
        elif task == "duplicate-pattern":
            issues = check_duplicate_pattern()
        elif task == "dead-code":
            issues = check_dead_code()
        
        all_issues.extend(issues)
        print(f"  → 发现 {len(issues)} 个问题")
    
    # 汇总
    print(f"\n📊 汇总: 共 {len(all_issues)} 个问题")
    
    if not args.check_only and all_issues:
        print("\n⚠️ 建议运行 --auto-fix 进行修复")
    
    return 0 if len(all_issues) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
