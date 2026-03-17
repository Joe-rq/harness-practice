# DRG Helper - 诊断相关分组助手

> 基于 Harness Engineering 实践的 DRG 分组辅助工具

## 项目简介

DRG Helper 是一个帮助医疗机构进行 DRG（Diagnosis Related Groups）分组的辅助工具。

## 功能特性

- 根据患者诊断和手术信息自动计算 DRG 分组
- 支持多种编码系统（ICD-10, ICD-9-CM-3）
- 提供分组结果解释和费用预测

## 技术栈

- Python 3.10+
- FastAPI (API 层)
- SQLite (数据存储)

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行服务
python src/api/main.py

# 运行测试
make test
```

## 项目结构

```
drg-helper/
├── src/
│   ├── api/          # API 层
│   ├── models/       # 数据模型
│   ├── services/     # 业务逻辑
│   └── utils/       # 工具函数
├── tests/           # 测试
└── docs/            # 文档
```

## 相关文档

- [API 文档](docs/api.md)
- [数据模型](docs/models.md)
- [DRG 分组规则](docs/drg-rules.md)
