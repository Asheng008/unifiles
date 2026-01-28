# unifiles 开发计划

## 1. 项目概述

### 1.1 项目目标
构建一个统一的文件操作库 `unifiles`，提供跨文件类型的统一接口，简化 Python 中对不同类型文件的读取、写入、抽取和查询操作。

### 1.2 MVP 范围
- **Excel 文件** (.xlsx, .xls): 读取、写入、获取工作表名称
- **PDF 文件** (.pdf): 提取文本、提取表格（基础）
- **Word 文档** (.docx): 读取、写入
- **SQLite 数据库** (.db, .sqlite): 查询、获取表结构、获取表名

### 1.3 技术栈
- **Python**: 3.9+（推荐 3.10+）
- **核心依赖**: pandas >=2.0.0, openpyxl >=3.1.0, pypdf >=3.0.0, python-docx >=1.0.0
- **开发工具**: pytest >=7.0.0, black >=23.0.0, mypy >=1.0.0
- **环境**: Windows 11, PowerShell

## 2. 开发阶段划分

### 阶段 0: 项目初始化（已完成）
- [x] 项目结构搭建
- [x] 技术需求文档编写
- [x] 开发规范文档编写

### 阶段 1: 基础设施搭建
**目标**: 搭建项目基础架构，包括项目配置、异常处理、测试框架

**任务清单**:
- [ ] 创建 `pyproject.toml` 配置文件
  - 配置项目元数据（名称、版本、描述）
  - 配置核心依赖（pandas, openpyxl, pypdf, python-docx）
  - 配置开发依赖（pytest, black, mypy）
  - 配置 Python 版本要求（>=3.9）
- [ ] 创建虚拟环境并安装依赖
  - 使用 PowerShell: `.\.venv\Scripts\Activate.ps1`
  - 安装依赖: `pip install -e ".[dev]"`
- [ ] 实现 `exceptions.py` 模块
  - `UnifilesError` 基础异常类
  - `FileFormatError` 文件格式错误
  - `FileReadError` 文件读取错误
  - `FileWriteError` 文件写入错误
- [ ] 创建 `src/unifiles/__init__.py`
  - 定义 `__version__ = "0.1.0"`
  - 预留导入位置（后续模块实现后添加）
- [ ] 配置开发工具
  - 配置 `black` 代码格式化
  - 配置 `mypy` 类型检查
  - 配置 `pytest` 测试框架
- [ ] 配置 Pre-commit Hooks
  - 安装 `pre-commit`: `pip install pre-commit`
  - 创建 `.pre-commit-config.yaml` 配置文件
    - 配置 `black` 自动格式化
    - 配置 `mypy` 类型检查
    - 配置 `pytest` 测试（可选）
  - 安装 hooks: `pre-commit install`
  - **目的**: 确保每次 commit 前自动执行代码质量检查，避免遗漏
- [ ] 配置 GitHub Actions CI/CD（可选但推荐）
  - 创建 `.github/workflows/ci.yml` 文件
  - 配置基本的 CI 流程：
    - 在 Push/PR 时自动运行
    - 设置 Python 3.9, 3.10, 3.11 多版本测试矩阵
    - 运行 `pytest` 测试
    - 运行 `mypy` 类型检查
    - 运行 `black --check` 格式化检查
  - **目的**: 提升代码集成信心，特别是频繁使用 AI 修改代码时
- [ ] 创建测试目录结构
  - `tests/__init__.py`
  - `tests/fixtures/test_files/` 目录

**验收标准**:
- [ ] `pyproject.toml` 配置完整，可通过 `pip install -e .` 安装
- [ ] 所有异常类定义完成，有完整的 docstring
- [ ] 开发工具配置完成，可正常运行格式化、类型检查、测试
- [ ] Pre-commit hooks 配置完成，`pre-commit run --all-files` 可正常运行
- [ ] GitHub Actions CI 配置完成（如适用），推送代码后能自动触发测试

**预计时间**: 1-2 天

---

### 阶段 2: Excel 模块开发
**目标**: 实现 Excel 文件的读取、写入和查询功能

**任务清单**:
- [ ] 实现 `excel.py` 模块
  - [ ] `read_excel(file_path, sheet_name=None) -> pd.DataFrame`
    - 支持指定工作表名称或索引
    - None 表示读取第一个工作表
    - 完整的类型注解（Python 3.9+ 风格）
    - Google 风格 docstring
    - 错误处理：FileNotFoundError, ValueError
  - [ ] `write_excel(data, file_path, sheet_name="Sheet1") -> None`
    - 支持单个 DataFrame 或字典（多工作表）
    - **明确约定**：覆盖整个文件，不保留原有其他 Sheet
    - 完整的类型注解
    - Google 风格 docstring
    - 错误处理：ValueError, PermissionError
  - [ ] `get_sheet_names(file_path) -> list[str]`
    - 返回所有工作表名称列表
    - 完整的类型注解
    - Google 风格 docstring
    - 错误处理：FileNotFoundError
- [ ] 编写 `tests/test_excel.py`
  - [ ] `test_read_excel_success` - 正常读取测试
  - [ ] `test_read_excel_sheet_name` - 指定工作表测试
  - [ ] `test_read_excel_file_not_found` - 文件不存在测试
  - [ ] `test_read_excel_invalid_sheet` - 无效工作表测试
  - [ ] `test_write_excel_dataframe` - 写入单个 DataFrame 测试
  - [ ] `test_write_excel_dict` - 写入多工作表测试
  - [ ] `test_write_excel_overwrite` - 覆盖文件测试
  - [ ] `test_get_sheet_names` - 获取工作表名称测试
  - [ ] `test_get_sheet_names_file_not_found` - 文件不存在测试
- [ ] 更新 `__init__.py` 导出 Excel 函数
  - `from .excel import read_excel, write_excel, get_sheet_names`

**开发步骤**（参考 AGENTS.md 工作流）:
1. **发现**: 使用 Context7 查阅 pandas、openpyxl 最新文档
2. **需求分析**: 确认函数签名和参数类型
3. **文档查阅**: 查询 pandas.read_excel、pandas.ExcelWriter、pandas.ExcelFile 用法
4. **实现**: 编写代码，确保类型注解完整
5. **测试**: 编写测试用例，覆盖正常和异常流程
6. **文档**: 更新 `__init__.py` 导出

**验收标准**:
- [ ] 所有函数实现完成，类型注解完整（Python 3.9+ 风格）
- [ ] 测试覆盖率 >= 80%
- [ ] 所有测试通过
- [ ] mypy 类型检查通过
- [ ] black 代码格式化通过

**预计时间**: 2-3 天

---

### 阶段 3: PDF 模块开发
**目标**: 实现 PDF 文件的文本提取和表格提取功能

**任务清单**:
- [ ] 实现 `pdf.py` 模块
  - [ ] `extract_text(file_path, page_range=None) -> str`
    - 支持指定页码范围（tuple[int, int]）
    - None 表示提取所有页面
    - 完整的类型注解
    - Google 风格 docstring
    - 错误处理：FileNotFoundError, ValueError
  - [ ] `extract_tables(file_path, page_range=None) -> list[pd.DataFrame]`
    - 基于 `pypdf` 实现
    - **MVP 说明**: 仅支持基础表格提取，复杂布局可能识别不准
    - 返回 DataFrame 列表
    - 完整的类型注解
    - Google 风格 docstring（包含 MVP 限制说明）
    - 错误处理：FileNotFoundError, ValueError
- [ ] 编写 `tests/test_pdf.py`
  - [ ] `test_extract_text_success` - 正常提取文本测试
  - [ ] `test_extract_text_page_range` - 指定页码范围测试
  - [ ] `test_extract_text_file_not_found` - 文件不存在测试
  - [ ] `test_extract_tables_success` - 基础表格提取测试
  - [ ] `test_extract_tables_page_range` - 指定页码范围测试
  - [ ] `test_extract_tables_file_not_found` - 文件不存在测试
  - [ ] `test_extract_tables_complex_layout` - 复杂布局测试（预期可能失败）
- [ ] 准备测试用的 PDF 文件
  - 简单文本 PDF（`tests/fixtures/test_files/simple.pdf`）
  - 包含基础表格的 PDF（`tests/fixtures/test_files/table.pdf`）
  - 复杂布局 PDF（`tests/fixtures/test_files/complex.pdf`，可选）
- [ ] 更新 `__init__.py` 导出 PDF 函数
  - `from .pdf import extract_text, extract_tables`

**开发步骤**:
1. **发现**: 使用 Context7 查阅 pypdf 最新文档
2. **需求分析**: 确认函数签名和参数类型
3. **文档查阅**: 查询 pypdf 文本提取和表格提取 API
4. **实现**: 编写代码，注意 MVP 限制说明
5. **测试**: 编写测试用例，注意复杂布局的限制
6. **文档**: 更新 `__init__.py` 导出

**验收标准**:
- [ ] 所有函数实现完成，类型注解完整
- [ ] 测试覆盖率 >= 80%
- [ ] 所有测试通过（复杂布局测试可标记为预期限制）
- [ ] mypy 类型检查通过
- [ ] black 代码格式化通过

**预计时间**: 2-3 天

---

### 阶段 4: Word 模块开发
**目标**: 实现 Word 文档的读取和写入功能

**任务清单**:
- [ ] 实现 `word.py` 模块
  - [ ] `read_docx(file_path) -> str`
    - 提取文档文本内容
    - 完整的类型注解
    - Google 风格 docstring
    - 错误处理：FileNotFoundError, ValueError
  - [ ] `write_docx(content, file_path, title=None) -> None`
    - 写入文本内容到 Word 文档
    - 支持可选标题
    - 完整的类型注解
    - Google 风格 docstring
    - 错误处理：ValueError, PermissionError
- [ ] 编写 `tests/test_word.py`
  - [ ] `test_read_docx_success` - 正常读取测试
  - [ ] `test_read_docx_file_not_found` - 文件不存在测试
  - [ ] `test_read_docx_invalid_format` - 无效格式测试
  - [ ] `test_write_docx_success` - 正常写入测试
  - [ ] `test_write_docx_with_title` - 带标题写入测试
  - [ ] `test_write_docx_permission_error` - 权限错误测试（模拟）
- [ ] 准备测试用的 Word 文档
  - 简单文档（`tests/fixtures/test_files/simple.docx`）
- [ ] 更新 `__init__.py` 导出 Word 函数
  - `from .word import read_docx, write_docx`

**开发步骤**:
1. **发现**: 使用 Context7 查阅 python-docx 最新文档
2. **需求分析**: 确认函数签名和参数类型
3. **文档查阅**: 查询 python-docx Document 类用法
4. **实现**: 编写代码
5. **测试**: 编写测试用例
6. **文档**: 更新 `__init__.py` 导出

**验收标准**:
- [ ] 所有函数实现完成，类型注解完整
- [ ] 测试覆盖率 >= 80%
- [ ] 所有测试通过
- [ ] mypy 类型检查通过
- [ ] black 代码格式化通过

**预计时间**: 1-2 天

---

### 阶段 5: SQLite 模块开发
**目标**: 实现 SQLite 数据库的查询和元数据获取功能

**任务清单**:
- [ ] 实现 `sqlite.py` 模块
  - [ ] `query(db_path, sql, params=None) -> pd.DataFrame`
    - 执行 SQL 查询
    - 支持参数化查询（tuple 或 dict）
    - 返回 DataFrame
    - 完整的类型注解
    - Google 风格 docstring
    - 错误处理：FileNotFoundError, sqlite3.Error
  - [ ] `get_schema(db_path, table_name) -> dict[str, str]`
    - 获取表结构（字段名到字段类型映射）
    - 完整的类型注解
    - Google 风格 docstring
    - 错误处理：FileNotFoundError, ValueError
  - [ ] `get_tables(db_path) -> list[str]`
    - 获取所有表名列表
    - 完整的类型注解
    - Google 风格 docstring
    - 错误处理：FileNotFoundError
- [ ] 编写 `tests/test_sqlite.py`
  - [ ] `test_query_success` - 正常查询测试
  - [ ] `test_query_with_params` - 参数化查询测试
  - [ ] `test_query_file_not_found` - 数据库不存在测试
  - [ ] `test_query_sql_error` - SQL 错误测试
  - [ ] `test_get_schema_success` - 获取表结构测试
  - [ ] `test_get_schema_table_not_found` - 表不存在测试
  - [ ] `test_get_tables_success` - 获取表名列表测试
  - [ ] `test_get_tables_file_not_found` - 数据库不存在测试
- [ ] 准备测试用的 SQLite 数据库
  - 创建测试数据库（`tests/fixtures/test_files/test.db`）
  - 包含示例表和测试数据
- [ ] 更新 `__init__.py` 导出 SQLite 函数
  - `from .sqlite import query, get_schema, get_tables`

**开发步骤**:
1. **发现**: 查阅 sqlite3 标准库文档
2. **需求分析**: 确认函数签名和参数类型
3. **文档查阅**: 查询 sqlite3 和 pandas.read_sql_query 用法
4. **实现**: 编写代码
5. **测试**: 编写测试用例
6. **文档**: 更新 `__init__.py` 导出

**验收标准**:
- [ ] 所有函数实现完成，类型注解完整
- [ ] 测试覆盖率 >= 80%
- [ ] 所有测试通过
- [ ] mypy 类型检查通过
- [ ] black 代码格式化通过

**预计时间**: 1-2 天

---

### 阶段 6: 集成测试与文档
**目标**: 完成集成测试、用户文档和发布准备

**任务清单**:
- [ ] 集成测试
  - [ ] 编写端到端测试用例
  - [ ] 测试各模块之间的协作
  - [ ] 性能测试（参考性能要求）
    - Excel 读取（1000行）< 1秒
    - PDF 文本提取（10页）< 2秒
    - Word 文档读取 < 0.5秒
    - SQLite 查询 < 0.1秒
- [ ] 用户文档
  - [ ] 编写 `README.md`
    - 项目介绍
    - 安装说明
    - 快速开始示例
    - API 概览
    - 贡献指南
  - [ ] 编写使用示例
    - Excel 操作示例
    - PDF 操作示例
    - Word 操作示例
    - SQLite 操作示例
- [ ] 代码质量检查
  - [ ] 运行所有测试：`pytest tests/ -v --cov=src/unifiles`
  - [ ] 确保测试覆盖率 >= 80%
  - [ ] 运行类型检查：`mypy src/unifiles/`
  - [ ] 运行代码格式化：`black --check src/ tests/`
  - [ ] 修复所有 lint 错误
  - [ ] 验证 Pre-commit hooks 正常工作：`pre-commit run --all-files`
  - [ ] 验证 GitHub Actions CI 通过（如已配置）
- [ ] 版本管理
  - [ ] 确认版本号：`0.1.0`
  - [ ] 更新 `__init__.py` 中的 `__version__`
  - [ ] 创建 git tag（如适用）
- [ ] 依赖锁定
  - [ ] 生成依赖锁文件（`poetry.lock` 或 `requirements.txt`）
  - [ ] 文档说明如何锁定依赖版本

**验收标准**:
- [ ] 所有集成测试通过
- [ ] 性能测试满足要求
- [ ] README.md 完整且清晰
- [ ] 测试覆盖率 >= 80%
- [ ] 类型检查通过
- [ ] 代码格式化通过
- [ ] 依赖锁文件已生成

**预计时间**: 2-3 天

---

## 3. 开发规范检查清单

每个模块开发完成后，必须检查以下项目（参考 AGENTS.md）：

- [ ] **工具**: 已查阅 Context7/RefTool 获取最新文档
- [ ] **环境**: 使用了 PowerShell 兼容路径和命令
- [ ] **Python版本**: 代码兼容 Python 3.9+
- [ ] **类型注解**: 使用了 Python 3.9+ 现代语法（`list[str]` 而非 `List[str]`）
- [ ] **类型完整性**: 所有函数参数和返回值都有 Type Hint
- [ ] **文档**: 所有公共函数都有完整的 docstring（Google 风格）
- [ ] **错误处理**: 使用了合适的异常类型，错误信息清晰
- [ ] **一致性**: API 设计与现有模块保持一致
- [ ] **测试**: 编写了测试用例，覆盖正常流程和异常流程
- [ ] **导入**: 在 `__init__.py` 中正确导出了新函数
- [ ] **Pre-commit**: 代码已通过 pre-commit hooks 检查（或已手动运行 `pre-commit run --all-files`）
- [ ] **CI**: 如已配置 GitHub Actions，确保 CI 通过

## 4. 测试策略

### 4.1 单元测试
- **框架**: pytest
- **覆盖率目标**: >= 80%
- **测试范围**:
  - 正常流程测试
  - 异常流程测试（文件不存在、格式错误、权限错误等）
  - 边界条件测试

### 4.2 测试文件组织
```
tests/
├── __init__.py
├── test_excel.py
├── test_pdf.py
├── test_word.py
├── test_sqlite.py
└── fixtures/
    └── test_files/  # 测试用的示例文件
        ├── simple.xlsx
        ├── simple.pdf
        ├── simple.docx
        └── test.db
```

### 4.3 测试运行命令
```powershell
# 激活虚拟环境
.\.venv\Scripts\Activate.ps1

# 运行所有测试
pytest tests/ -v

# 运行测试并显示覆盖率
pytest tests/ -v --cov=src/unifiles --cov-report=html

# 运行特定模块测试
pytest tests/test_excel.py -v
```

## 5. 代码质量工具

### 5.1 类型检查
```powershell
# 运行 mypy 类型检查
mypy src/unifiles/
```

### 5.2 代码格式化
```powershell
# 检查代码格式
black --check src/ tests/

# 自动格式化代码
black src/ tests/
```

### 5.3 测试覆盖率
```powershell
# 生成覆盖率报告
pytest tests/ --cov=src/unifiles --cov-report=html
```

### 5.4 Pre-commit Hooks
```powershell
# 安装 pre-commit hooks（首次设置）
pre-commit install

# 手动运行所有 hooks（测试配置）
pre-commit run --all-files

# 运行特定 hook
pre-commit run black --all-files
pre-commit run mypy --all-files
```

**说明**: Pre-commit hooks 会在每次 `git commit` 时自动运行，确保代码质量。如果检查失败，commit 会被阻止，需要修复后重新提交。

### 5.5 CI/CD 自动化（GitHub Actions）
CI/CD 流程会在以下情况自动触发：
- Push 代码到主分支
- 创建 Pull Request
- 手动触发（workflow_dispatch）

**CI 流程包括**:
1. 设置 Python 环境（3.9, 3.10, 3.11）
2. 安装依赖
3. 运行 `pytest` 测试
4. 运行 `mypy` 类型检查
5. 运行 `black --check` 格式化检查

**查看 CI 状态**: 在 GitHub 仓库的 "Actions" 标签页查看运行结果。

## 6. 里程碑

| 里程碑 | 阶段 | 预计完成时间 | 状态 |
|--------|------|-------------|------|
| M0: 项目初始化 | 阶段 0 | 已完成 | ✅ |
| M1: 基础设施完成 | 阶段 1 | 第 1-2 天 | ⏳ |
| M2: Excel 模块完成 | 阶段 2 | 第 3-5 天 | ⏳ |
| M3: PDF 模块完成 | 阶段 3 | 第 6-8 天 | ⏳ |
| M4: Word 模块完成 | 阶段 4 | 第 9-10 天 | ⏳ |
| M5: SQLite 模块完成 | 阶段 5 | 第 11-12 天 | ⏳ |
| M6: MVP 发布准备 | 阶段 6 | 第 13-15 天 | ⏳ |

**总预计时间**: 约 15 个工作日（3 周）

## 7. 后续版本规划

### v0.2.0: 扩展文件类型支持
- CSV 文件支持
- JSON 文件支持

### v0.3.0: 图片文件处理
- PIL/Pillow 集成
- 图片读取、写入、格式转换

### v0.4.0: 文件格式转换
- Excel 转 CSV
- PDF 转 Word
- 等格式转换功能

### v0.5.0: 性能优化
- 批量处理功能
- 异步 I/O 支持（可选）
- 内存优化

## 8. 风险与应对

### 8.1 技术风险
- **PDF 表格提取效果不佳**
  - **风险**: pypdf 对复杂表格识别能力有限
  - **应对**: MVP 阶段明确说明限制，后续版本考虑引入 pdfplumber

- **依赖版本冲突**
  - **风险**: 不同依赖库版本可能冲突
  - **应对**: 使用依赖锁文件，定期更新和测试

### 8.2 开发风险
- **时间估算不准确**
  - **风险**: 实际开发时间可能超出预期
  - **应对**: 每个阶段设置缓冲时间，优先完成核心功能

- **测试覆盖率不足**
  - **风险**: 测试用例可能遗漏边界情况
  - **应对**: 代码审查，使用覆盖率工具监控

## 9. 参考资料

- **技术需求文档**: `TECH_REQUIREMENTS.md`
- **开发规范文档**: `AGENTS.md`
- **项目结构**: 参考 TECH_REQUIREMENTS.md 第 3.1 节
- **API 设计**: 参考 TECH_REQUIREMENTS.md 第 4 节
- **开发工作流**: 参考 AGENTS.md 第 7 节

---

**最后更新**: 2026-01-28  
**文档版本**: 1.0
