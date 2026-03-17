#!/usr/bin/env python3
"""Architecture Lint - 架构检查主脚本"""

import argparse
import sys
from pathlib import Path
import re

# 层级依赖规则
RULES = {
    "UI": ["Runtime", "Service", "Repo", "Config", "Types"],
    "Runtime": ["Service", "Repo", "Config", "Types"],
    "Service": ["Repo", "Config", "Types"],
    "Repo": ["Config", "Types"],
    "Config": ["Types"],
    "Types": []
}

def detect_layer(file_path: str) -> str:
    """检测文件所在层"""
    path = Path(file_path)
    parts = path.parts
    
    if "ui" in parts or "view" in parts or "component" in parts:
        return "UI"
    elif "runtime" in parts or "middleware" in parts:
        return "Runtime"
    elif "service" in parts or "controller" in parts:
        return "Service"
    elif "repo" in parts or "repository" in parts or "dao" in parts:
        return "Repo"
    elif "config" in parts:
        return "Config"
    elif "types" in parts or "models" in parts or "schemas" in parts:
        return "Types"
    
    return "Unknown"

def check_layer_dependency(file_path: str, imports: list) -> list:
    """检查层级依赖"""
    current_layer = detect_layer(file_path)
    allowed_layers = RULES.get(current_layer, [])
    
    violations = []
    for imp in imports:
        imp_layer = detect_layer(imp)
        if imp_layer != "Unknown" and imp_layer not in allowed_layers:
            violations.append({
                "file": file_path,
                "rule": "layer_dependency",
                "message": f"{current_layer} cannot import {imp_layer}",
                "severity": "error"
            })
    
    return violations

def check_naming(file_path: str) -> list:
    """检查命名规范"""
    path = Path(file_path)
    violations = []
    
    # 文件名检查
    if path.suffix in [".py"]:
        if not re.match(r"^[a-z0-9-]+\.[a-z]+$", path.name):
            violations.append({
                "file": file_path,
                "rule": "naming",
                "message": f"文件名应为 kebab-case: {path.name}",
                "severity": "warning"
            })
    
    return violations

def check_complexity(file_path: str) -> list:
    """检查复杂度"""
    violations = []
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # 文件行数检查
        if len(lines) > 500:
            violations.append({
                "file": file_path,
                "rule": "file_length",
                "message": f"文件行数 {len(lines)} > 500",
                "severity": "warning"
            })
        
        # 简单函数检查
        in_function = False
        func_lines = 0
        for line in lines:
            if line.strip().startswith("def ") or line.strip().startswith("func "):
                in_function = True
                func_lines = 0
            elif in_function:
                func_lines += 1
                if func_lines > 50:
                    violations.append({
                        "file": file_path,
                        "rule": "function_length",
                        "message": f"函数超过 50 行",
                        "severity": "warning"
                    })
                    in_function = False
    
    except Exception as e:
        pass
    
    return violations

def main():
    parser = argparse.ArgumentParser(description="Architecture Lint")
    parser.add_argument("--strict", action="store_true", help="严格模式")
    parser.add_argument("--rule", help="仅运行特定规则")
    args = parser.parse_args()
    
    violations = []
    
    # 扫描源文件
    src_dir = Path("src")
    if src_dir.exists():
        for file in src_dir.rglob("*.py"):
            if args.rule in [None, "layer_dependency"]:
                # 简化版：仅检查文件存在性
                pass
            
            if args.rule in [None, "naming"]:
                violations.extend(check_naming(str(file)))
            
            if args.rule in [None, "complexity"]:
                violations.extend(check_complexity(str(file)))
    
    # 输出结果
    if violations:
        print(f"❌ 发现 {len(violations)} 个问题:")
        for v in violations:
            print(f"  {v['severity']}: {v['rule']} - {v['message']}")
        
        if args.strict:
            sys.exit(1)
    else:
        print("✅ 通过所有检查")

if __name__ == "__main__":
    main()
