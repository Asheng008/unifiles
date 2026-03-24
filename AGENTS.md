# AGENTS.md - Agent 操作指南

> **首先阅读**: 本文件管理本仓库中所有 AI Agent 的行为。

## 项目概述

- **项目**: `unifiles` — Python 文件操作工具库 (Excel/PDF/Word/SQLite/JSON/YAML/TXT)
- **技术栈**: Python 3.10+, pandas, openpyxl, pypdf, python-docx, PyYAML
- **标准**: 类型安全，Google 风格 docstring，SOLID 原则

## 环境要求（关键）

- **操作系统**: Linux — 仅限 Bash。禁止 Windows 命令（`dir`、`$env:`、`type`）。
- **Python**: 必须使用 venv 绝对路径。禁止系统 Python。
  ```bash
  export PY="/home/wen/pro/unifiles/.venv/bin/python"
  ```
- **编码**: UTF-8（默认支持中文，无需额外设置）。

## 构建/检查/测试命令

```bash
source .venv/bin/activate              # 或直接使用 $PY

# 格式化
black --check src/ tests/              # 仅检查
black src/ tests/                      # 自动修复

# 类型检查
mypy src/unifiles/

# 测试
pytest                                 # 全部测试 + 覆盖率
pytest tests/test_excel.py -v          # 单个文件
pytest tests/test_excel.py::test_read_excel_success -v  # 单个函数
pytest -k "read_excel" -v              # 关键词匹配
pytest -m "not slow" -v                # 跳过慢速测试
```

**提交前 CI 检查**（三项必须全部通过）:
```bash
black --check src/ tests/ || exit 1
mypy src/unifiles/ || exit 1
pytest || exit 1
```

## 代码规范

详见 [docs/CODE_STYLE.md](docs/CODE_STYLE.md)，包含：
- 类型注解（Python 3.10+ 现代语法）
- 导入顺序
- Docstring（Google 风格，中文）
- 错误处理
- 命名规范
- 测试规范
- API 设计规则

## 模块结构

```
src/unifiles/
├── __init__.py     # 导出所有公共 API
├── exceptions.py   # 自定义异常
├── excel.py        # pandas + openpyxl
├── pdf.py          # pypdf
├── word.py         # python-docx
├── sqlite.py       # sqlite3
├── json.py         # json (标准库)
├── yaml.py         # PyYAML
└── txt.py          # 文本 I/O
```

## 禁止事项

- ❌ 系统 Python 或不使用 venv 的 `pip install`
- ❌ Bash 中使用 Windows 命令（`dir`、`$env:`、`type`）
- ❌ 旧式类型注解（`List[str]`、`Union[...]`、`Optional[...]`）
- ❌ `as any`、`@ts-ignore`、类型错误抑制
- ❌ 修改函数签名而不更新测试
- ❌ 跳过文件操作的错误处理
- ❌ 硬编码文件路径 — 必须参数化

## 参考资料

- **代码规范**: [docs/CODE_STYLE.md](docs/CODE_STYLE.md)
- **配置**: `pyproject.toml`（black: 88 字符，mypy: 严格，pytest: 覆盖率）
- **需求文档**: `TECH_REQUIREMENTS.md` — 功能规格
- **开发计划**: `DEVELOPMENT_PLAN.md` — 开发路线图
