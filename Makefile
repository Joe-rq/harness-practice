#!/bin/bash
# Harness Practice - 常用命令

.PHONY: help lint test clean report install

help:
	@echo "Harness Practice - 可用命令"
	@echo ""
	@echo "  make lint       运行架构检查"
	@echo "  make test       运行测试"
	@echo "  make clean      运行清洁 Agent"
	@echo "  make report     生成进度报告"
	@echo "  make install    安装依赖"

lint:
	@echo "运行架构 Lint..."
	@python3 .harness/lint-rules/run_all.py

test:
	@echo "运行测试..."
	@python3 -m pytest tests/ -v

clean:
	@echo "运行清洁 Agent..."
	@python3 -m .harness.tasks.cleanup --auto-fix

report:
	@echo "生成进度报告..."
	@python3 .harness/scripts/generate_report.py

install:
	@echo "安装依赖..."
	npm install
	pip install -r requirements.txt
