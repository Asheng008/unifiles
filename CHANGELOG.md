# Changelog

所有显著变更都会记录在此文档中，格式参考语义化版本规范（`MAJOR.MINOR.PATCH`），并结合 `docs/04-版本管理与发布节奏.md` 中的约定执行。

> 约定：从**下一个版本**开始（例如 `0.2.0`），每次发布前必须先在此文档中补充对应版本的小节，然后再修改版本号、打 Tag、发布。

## [Unreleased]

- （在开发下一个版本时，将改动先记录在这里；发布时再移动到对应版本小节）

## [0.4.0] - 2026-03-24

### Added

- Word 模块新增功能：
  - `extract_text_docx()` - 提取完整文本，段落和表格按文档顺序输出，表格转为 Markdown 格式
  - `extract_tables_docx()` - 提取所有表格，支持 `format='md'`（Markdown）和 `format='list'`（二维列表）
  - `extract_images_docx()` - 提取所有图片，自动保存到指定目录（默认 `./pics/`）
  - `inspect_docx()` - 综合检查文档元素，返回段落、表格、图片的统计信息

### Changed

- 重构 `word.py` 为 `word/` 包结构，职责分离更清晰：
  - `word/_table.py` - 表格处理辅助函数（`table_to_list`, `list_to_markdown`）
  - `word/_legacy.py` - 废弃的 `read_docx` 函数
  - `word/write.py` - 写入功能
  - `word/extract.py` - 提取功能
  - `word/inspect.py` - 检查功能
- 重构 `tests/test_word.py` 为 `tests/word/` 包结构
- AGENTS.md 支持 Linux/macOS 和 Windows 双平台

### Deprecated

- `read_docx()` - 已废弃，请使用 `extract_text_docx()` 替代

## [0.3.1] - 2026-01-30

### Fixed

- 修复 `fillna()` 方法在某些 pandas 版本中的兼容性问题
  - 将 `fillna(None)` 改为 `fillna(value=None)`，明确指定参数名
  - 影响函数：`get_excel_info()`, `get_sheet_info()`, `get_database_info()`
  - 解决了 GitHub Actions CI 中出现的 "Must specify a fill 'value' or 'method'" 错误

## [0.3.0] - 2026-01-30

### Added

- Excel 模块新增功能：
  - `get_column_names()` - 获取 Excel 工作表的列名，支持指定 header 行或预览前几行
  - `get_sheet_info()` - 获取单个工作表的详细信息（行数、列数、列名、数据预览）
  - `get_excel_info()` - 获取整个 Excel 文件的完整信息（所有工作表信息、文件大小等）
- SQLite 模块新增功能：
  - `get_database_info()` - 获取数据库的完整信息（文件大小、表数量、每个表的详细信息，可选数据预览）

## [0.2.0] - 2026-01-29

### Changed

- **破坏性变更**：将最低 Python 版本要求从 3.9 提升到 3.10
  - 代码中使用了 Python 3.10+ 的联合类型语法（`|` 运算符），不再兼容 Python 3.9
  - 更新 CI 工作流，移除 Python 3.9 测试矩阵
  - 更新 `pyproject.toml` 中的 `requires-python` 和 classifiers

### Added

- 添加 GitHub Actions CI 工作流（`.github/workflows/ci.yml`）
  - 自动运行代码格式检查（black）
  - 自动运行类型检查（mypy）
  - 自动运行单元测试（pytest）
  - 自动构建分发包验证
  - 支持 Python 3.10 / 3.11 / 3.12 多版本测试

## [0.1.0] - 2026-01-28

### Added

- 首个公开版本，提供 Excel / PDF / Word / SQLite 的统一文件操作能力：
  - Excel 模块：`read_excel` / `write_excel` / `get_sheet_names`
  - PDF 模块：`extract_text` / `extract_tables`（基础表格抽取，复杂版式存在已知限制）
  - Word 模块：`read_docx` / `write_docx`
  - SQLite 模块：`query` / `get_schema` / `get_tables`
- 基本单元测试、性能测试与测试用示例文件。
- 本地发布脚本与技术文档：
  - `docs/01-发布Python包到PyPI.md`
  - `publish_pypi.bat`
- GitHub Actions 相关技术文档（CI 与自动发布设计）：
  - `docs/02-使用GitHub-Actions搭建CI流水线.md`
  - `docs/03-用GitHub-Actions自动发布到PyPI.md`
  - `docs/04-版本管理与发布节奏.md`
