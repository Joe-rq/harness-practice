#!/usr/bin/env python3
"""Code Review Script - 主审查脚本"""

import argparse
import subprocess
import os
from datetime import datetime
from pathlib import Path

REVIEW_DIR = Path(".harness/reviews")
REVIEW_DIR.mkdir(parents=True, exist_ok=True)

def run_security_scan(files):
    """安全扫描"""
    results = []
    
    # 硬编码密钥
    patterns = ["password", "api_key", "secret", "token", "sk-"]
    for pattern in patterns:
        cmd = f"grep -rn '{pattern}' --include='*.py' --include='*.ts' {files}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            results.append(f"### 密钥风险: {pattern}\n```\n{result.stdout}\n```")
    
    return results

def run_architecture_check(files):
    """架构检查"""
    results = []
    
    # 层级依赖检查
    cmd = "python .harness/lint-rules/check_layer_dependency.py"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        results.append(f"### 架构检查\n```\n{result.stdout}\n```")
    
    return results

def run_test_check():
    """测试检查"""
    results = []
    
    # 检查测试存在
    if not Path("tests").exists():
        results.append("⚠️ 未找到 tests/ 目录")
    
    # 运行测试
    result = subprocess.run("make test", shell=True, capture_output=True, text=True)
    results.append(f"### 测试结果\n```\n{result.stdout}\n```")
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Code Review Script")
    parser.add_argument("--files", required=True, help="要审查的文件")
    parser.add_argument("--mode", default="full", choices=["fast", "full"], help="审查模式")
    args = parser.parse_args()
    
    results = []
    results.append(f"# Code Review Report\n")
    results.append(f"**时间**: {datetime.now().isoformat()}\n")
    results.append(f"**文件**: {args.files}\n")
    results.append(f"**模式**: {args.mode}\n")
    
    # 安全扫描
    results.append("\n## 安全扫描\n")
    results.extend(run_security_scan(args.files))
    
    if args.mode == "full":
        # 架构检查
        results.append("\n## 架构检查\n")
        results.extend(run_architecture_check(args.files))
        
        # 测试检查
        results.append("\n## 测试检查\n")
        results.extend(run_test_check())
    
    # 写入报告
    report = "\n".join(results)
    report_file = REVIEW_DIR / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    report_file.write_text(report)
    
    # 创建 latest 链接
    latest_link = REVIEW_DIR / "latest.md"
    latest_link.write_text(report)
    
    print(report)
    print(f"\n报告已保存至: {report_file}")

if __name__ == "__main__":
    main()
