# unifiles MVP 技术需求文档

## 1. 项目概述

### 1.1 项目名称
unifiles

### 1.2 项目定位
unifiles 是一个统一的文件操作库，提供跨文件类型的统一接口，简化Python中对不同类型文件的读取、写入、抽取和查询操作。

### 1.3 核心价值
- **统一接口**：为不同文件类型提供一致的API设计
- **易于使用**：简化常见文件操作，降低学习成本
- **模块化设计**：每种文件类型独立模块，按需导入
- **扩展性强**：易于添加新的文件类型支持

## 2. MVP 功能范围

### 2.1 支持的文件类型（MVP阶段）

#### 2.1.1 Excel文件 (.xlsx, .xls)
- **读取**：读取Excel文件，支持指定工作表
- **写入**：写入数据到Excel文件
- **查询**：获取工作表名称列表

#### 2.1.2 PDF文件 (.pdf)
- **抽取**：提取PDF文本内容
- **抽取**：提取PDF中的表格数据  
  **MVP 说明**：MVP 阶段使用 `pypdf` 实现，**仅支持基础表格提取**；复杂布局、多列、合并单元格等场景可能识别不准。若需更好效果，后续版本可考虑引入 `pdfplumber` 等库。

#### 2.1.3 Word文档 (.docx)
- **读取**：读取Word文档内容
- **写入**：写入内容到Word文档

#### 2.1.4 SQLite数据库 (.db, .sqlite)
- **查询**：执行SQL查询
- **查询**：获取数据库表结构（schema）
- **查询**：获取数据库表名列表

### 2.2 功能边界（MVP阶段不包含）
- CSV文件（后续版本）
- JSON文件（后续版本）
- 图片文件（后续版本）
- 压缩文件（后续版本）
- 文件格式转换（后续版本）

## 3. 技术架构

### 3.1 项目结构
```
unifiles/
├── pyproject.toml          # 项目配置和依赖管理
├── README.md               # 项目说明文档
├── TECH_REQUIREMENTS.md    # 技术需求文档（本文档）
└── src/
    └── unifiles/
        ├── __init__.py     # 包初始化，导出主要API
        ├── excel.py        # Excel文件操作模块
        ├── pdf.py          # PDF文件操作模块
        ├── word.py         # Word文档操作模块
        ├── sqlite.py       # SQLite数据库操作模块
        └── exceptions.py   # 自定义异常类
```

### 3.2 依赖管理

#### 3.2.1 核心依赖
- **pandas**: >=2.0.0 - Excel文件读写和数据处理
- **openpyxl**: >=3.1.0 - Excel文件格式支持
- **pypdf**: >=3.0.0 - PDF文件处理
- **python-docx**: >=1.0.0 - Word文档处理

#### 3.2.2 开发依赖（可选）
- **pytest**: >=7.0.0 - 单元测试框架
- **black**: >=23.0.0 - 代码格式化
- **mypy**: >=1.0.0 - 类型检查

#### 3.2.3 依赖版本与锁定
- **声明方式**：`pyproject.toml` 中核心依赖使用下限约束（如 `>=2.0.0`）便于兼容。
- **环境一致性**：实际开发与部署建议通过 **锁文件** 固定版本，例如：
  - 使用 **Poetry** 时保留并提交 `poetry.lock`
  - 使用 **pip** 时可用 `pip-tools`（`pip-compile` 生成 `requirements.txt`）或 `uv lock` 等
- 这样可保证不同环境复现一致，避免因依赖升级导致行为变化。

### 3.3 Python版本要求
- Python >= 3.9（推荐 3.10+，以使用联合类型 `|` 运算符）

## 4. 模块设计

### 4.1 excel.py 模块

#### 4.1.1 read_excel()
**功能**：读取Excel文件内容

**函数签名**：
```python
def read_excel(file_path: str, sheet_name: str | int | None = None) -> pd.DataFrame
```

**参数**：
- `file_path` (str): Excel文件路径
- `sheet_name` (str | int | None): 工作表名称或索引，None表示读取第一个工作表

**返回**：
- `pd.DataFrame`: 包含Excel数据的DataFrame对象

**异常**：
- `FileNotFoundError`: 文件不存在
- `ValueError`: 工作表不存在或无效

#### 4.1.2 write_excel()
**功能**：将数据写入Excel文件

**函数签名**：
```python
def write_excel(data: pd.DataFrame | dict[str, pd.DataFrame], file_path: str, sheet_name: str = "Sheet1") -> None
```

**参数**：
- `data` (pd.DataFrame | dict[str, pd.DataFrame]): 要写入的数据，可以是单个DataFrame或字典（多工作表）
- `file_path` (str): 输出Excel文件路径
- `sheet_name` (str): 工作表名称（当data为DataFrame时使用）

**写入语义（MVP 明确约定）**：
- **默认行为**：**覆盖整个目标文件**。若 `file_path` 已存在，则先清空再写入当前 `data`，不保留原文件中的其他 Sheet。
- 即：每次调用均生成“仅包含本次传入数据”的完整 Excel 文件；**不**支持“在现有文件上追加新 Sheet”的追加模式。若需追加，应由调用方先 `read_excel` 再合并后调用 `write_excel`。

**返回**：
- None

**异常**：
- `ValueError`: 数据格式无效
- `PermissionError`: 文件权限不足

#### 4.1.3 get_sheet_names()
**功能**：获取Excel文件中的所有工作表名称

**函数签名**：
```python
def get_sheet_names(file_path: str) -> list[str]
```

**参数**：
- `file_path` (str): Excel文件路径

**返回**：
- `list[str]`: 工作表名称列表

**异常**：
- `FileNotFoundError`: 文件不存在

### 4.2 pdf.py 模块

#### 4.2.1 extract_text()
**功能**：从PDF文件中提取文本内容

**函数签名**：
```python
def extract_text(file_path: str, page_range: tuple[int, int] | None = None) -> str
```

**参数**：
- `file_path` (str): PDF文件路径
- `page_range` (tuple[int, int] | None): 页码范围(start, end)，None表示提取所有页面

**返回**：
- `str`: 提取的文本内容

**异常**：
- `FileNotFoundError`: 文件不存在
- `ValueError`: PDF文件损坏或无法读取

#### 4.2.2 extract_tables()
**功能**：从PDF文件中提取表格数据

**函数签名**：
```python
def extract_tables(file_path: str, page_range: tuple[int, int] | None = None) -> list[pd.DataFrame]
```

**参数**：
- `file_path` (str): PDF文件路径
- `page_range` (tuple[int, int] | None): 页码范围(start, end)，None表示提取所有页面

**返回**：
- `list[pd.DataFrame]`: 提取的表格列表，每个表格为一个DataFrame

**MVP 说明**：基于 `pypdf` 实现，**仅支持基础表格提取**；复杂布局、多列、合并单元格等可能识别不准，属预期限制。后续版本可考虑引入 `pdfplumber` 以提升效果。

**异常**：
- `FileNotFoundError`: 文件不存在
- `ValueError`: PDF文件损坏或无法读取

### 4.3 word.py 模块

#### 4.3.1 read_docx()
**功能**：读取Word文档内容

**函数签名**：
```python
def read_docx(file_path: str) -> str
```

**参数**：
- `file_path` (str): Word文档路径

**返回**：
- `str`: 文档的文本内容

**异常**：
- `FileNotFoundError`: 文件不存在
- `ValueError`: 文件格式无效

#### 4.3.2 write_docx()
**功能**：将内容写入Word文档

**函数签名**：
```python
def write_docx(content: str, file_path: str, title: str | None = None) -> None
```

**参数**：
- `content` (str): 要写入的文本内容
- `file_path` (str): 输出Word文档路径
- `title` (str | None): 文档标题（可选）

**返回**：
- None

**异常**：
- `ValueError`: 内容格式无效
- `PermissionError`: 文件权限不足

### 4.4 sqlite.py 模块

#### 4.4.1 query()
**功能**：执行SQL查询

**函数签名**：
```python
def query(db_path: str, sql: str, params: tuple | dict | None = None) -> pd.DataFrame
```

**参数**：
- `db_path` (str): SQLite数据库文件路径
- `sql` (str): SQL查询语句
- `params` (tuple | dict | None): 查询参数（用于参数化查询）

**返回**：
- `pd.DataFrame`: 查询结果

**异常**：
- `FileNotFoundError`: 数据库文件不存在
- `sqlite3.Error`: SQL执行错误

#### 4.4.2 get_schema()
**功能**：获取数据库表结构

**函数签名**：
```python
def get_schema(db_path: str, table_name: str) -> dict[str, str]
```

**参数**：
- `db_path` (str): SQLite数据库文件路径
- `table_name` (str): 表名

**返回**：
- `dict[str, str]`: 字段名到字段类型的映射

**异常**：
- `FileNotFoundError`: 数据库文件不存在
- `ValueError`: 表不存在

#### 4.4.3 get_tables()
**功能**：获取数据库中的所有表名

**函数签名**：
```python
def get_tables(db_path: str) -> list[str]
```

**参数**：
- `db_path` (str): SQLite数据库文件路径

**返回**：
- `list[str]`: 表名列表

**异常**：
- `FileNotFoundError`: 数据库文件不存在

### 4.5 __init__.py 模块

**功能**：包初始化，导出主要API

**导出内容**：
```python
# Excel模块
from .excel import read_excel, write_excel, get_sheet_names

# PDF模块
from .pdf import extract_text, extract_tables

# Word模块
from .word import read_docx, write_docx

# SQLite模块
from .sqlite import query, get_schema, get_tables

__version__ = "0.1.0"
```

### 4.6 exceptions.py 模块

**功能**：定义自定义异常类

**异常类**：
```python
class UnifilesError(Exception):
    """unifiles基础异常类"""
    pass

class FileFormatError(UnifilesError):
    """文件格式错误"""
    pass

class FileReadError(UnifilesError):
    """文件读取错误"""
    pass

class FileWriteError(UnifilesError):
    """文件写入错误"""
    pass
```

## 5. API设计原则

### 5.1 一致性原则
- 所有读取函数统一使用 `file_path` 作为第一个参数
- 所有写入函数统一使用 `data/content` 作为第一个参数，`file_path` 作为第二个参数
- 返回类型明确：DataFrame用于表格数据，str用于文本数据，list用于列表数据

### 5.2 错误处理
- 使用Python标准异常（FileNotFoundError, ValueError等）
- 提供自定义异常类用于库特定错误
- 异常信息清晰，便于调试

### 5.3 类型提示
- 所有函数提供完整的类型提示（Type Hints）
- 使用 Python 3.9+ 现代类型注解语法：`list[str]`、`dict[str, str]`、`tuple[int, int]`、`str | None` 等，避免 `typing.List`、`typing.Union` 等旧式写法

## 6. 使用示例

### 6.1 Excel操作示例
```python
import unifiles

# 读取Excel文件
df = unifiles.read_excel("data.xlsx", sheet_name="Sheet1")

# 获取所有工作表名称
sheets = unifiles.get_sheet_names("data.xlsx")

# 写入Excel文件
unifiles.write_excel(df, "output.xlsx", sheet_name="Results")
```

### 6.2 PDF操作示例
```python
import unifiles

# 提取PDF文本
text = unifiles.extract_text("document.pdf")

# 提取PDF表格
tables = unifiles.extract_tables("document.pdf", page_range=(1, 5))
```

### 6.3 Word操作示例
```python
import unifiles

# 读取Word文档
content = unifiles.read_docx("document.docx")

# 写入Word文档
unifiles.write_docx("Hello World", "output.docx", title="My Document")
```

### 6.4 SQLite操作示例
```python
import unifiles

# 执行查询
df = unifiles.query("database.db", "SELECT * FROM users WHERE age > ?", (18,))

# 获取表结构
schema = unifiles.get_schema("database.db", "users")

# 获取所有表名
tables = unifiles.get_tables("database.db")
```

## 7. 开发计划

### 7.1 MVP阶段（已完成）
- [x] 项目结构搭建
- [x] Excel模块实现
- [x] PDF模块实现
- [x] Word模块实现
- [x] SQLite模块实现
- [x] 基础测试用例
- [x] 文档编写（README、TECH_REQUIREMENTS、DEVELOPMENT_PLAN 及基础使用文档）

### 7.2 后续版本规划
- **v0.2.0**: 添加CSV、JSON文件支持
- **v0.3.0**: 添加图片文件处理（PIL/Pillow）
- **v0.4.0**: 添加文件格式转换功能
- **v0.5.0**: 性能优化和批量处理功能

## 8. 测试要求

### 8.1 单元测试
- 每个模块至少80%代码覆盖率
- 测试用例覆盖正常流程和异常流程
- 使用pytest框架

### 8.2 测试文件结构
```
tests/
├── __init__.py
├── test_excel.py
├── test_pdf.py
├── test_word.py
├── test_sqlite.py
└── fixtures/
    └── test_files/  # 测试用的示例文件
```

## 9. 文档要求

### 9.1 代码文档
- 所有公共函数提供docstring（Google风格）
- 包含参数说明、返回值说明、异常说明和使用示例

### 9.2 用户文档
- README.md：项目介绍、安装说明、快速开始
- API文档：详细的函数说明和示例

## 10. 性能要求

### 10.1 MVP阶段性能目标
- Excel文件读取（1000行）：< 1秒
- PDF文本提取（10页）：< 2秒
- Word文档读取（普通文档）：< 0.5秒
- SQLite查询（简单查询）：< 0.1秒

### 10.2 内存要求
- 支持处理中等大小的文件（< 100MB）
- 避免一次性加载超大文件到内存

## 11. 兼容性要求

### 11.1 操作系统
- Windows 10+
- Linux（主流发行版）
- macOS 10.14+

### 11.2 Python版本
- Python 3.9+
- 使用 Python 3.9+ 内置泛型与 3.10+ 联合类型 `|` 语法，不依赖 `typing.List`/`typing.Union` 等旧式注解

## 12. 许可证
本项目采用 MIT License，详见仓库根目录的 `LICENSE` 文件。
