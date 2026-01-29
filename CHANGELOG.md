# Changelog

所有显著变更都会记录在此文档中，格式参考语义化版本规范（`MAJOR.MINOR.PATCH`），并结合 `docs/04-版本管理与发布节奏.md` 中的约定执行。

> 约定：从**下一个版本**开始（例如 `0.2.0`），每次发布前必须先在此文档中补充对应版本的小节，然后再修改版本号、打 Tag、发布。

## [Unreleased]

- （在开发下一个版本时，将改动先记录在这里；发布时再移动到对应版本小节）

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
