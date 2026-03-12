# unifiles API 参考

本文档列举 `unifiles` 包对外暴露的全部 API（函数与异常类），便于查阅与集成。

包版本可通过 `unifiles.__version__` 获取。

**目录**

- [Excel 模块 (excel)](#excel-模块-excel)
  - `read_excel`
  - `write_excel`
  - `get_sheet_names`
  - `get_column_names`
  - `get_sheet_info`
  - `get_excel_info`
- [Word 模块 (word)](#word-模块-word)
  - `read_docx`
  - `write_docx`
- [TXT/文本 模块 (txt)](#txt文本-模块-txt)
  - `read_txt`
  - `write_txt`
- [SQLite 模块 (sqlite)](#sqlite-模块-sqlite)
  - `query`
  - `get_schema`
  - `get_tables`
  - `get_database_info`
- [PDF 模块 (pdf)](#pdf-模块-pdf)
  - `extract_text`
  - `extract_tables`
- [异常类 (exceptions)](#异常类-exceptions)
  - `UnifilesError`
  - `FileFormatError`
  - `FileReadError`
  - `FileWriteError`
- [使用示例](#使用示例)

---

## Excel 模块 (excel)

- **read_excel** `(file_path, sheet_name=None) -> pd.DataFrame`  
  读取 Excel 文件内容，返回 DataFrame。`sheet_name` 为工作表名或索引，`None` 表示第一个工作表。

- **write_excel** `(data, file_path, sheet_name="Sheet1") -> None`  
  将数据写入 Excel 文件。`data` 可为单个 DataFrame 或「工作表名 → DataFrame」的字典；会覆盖目标文件，不保留原有其他 Sheet。

- **get_sheet_names** `(file_path) -> list[str]`  
  返回该 Excel 文件中所有工作表的名称列表。

- **get_column_names** `(file_path, sheet_name=None, header=0, peek_rows=0) -> list[str] | dict`  
  获取指定工作表的列名。可指定 `header`（列名所在行，0-based）或设 `peek_rows>0` 预览前几行再判断列名行。

- **get_sheet_info** `(file_path, sheet_name=None, preview_rows=5) -> dict`  
  返回单个工作表的信息：名称、行数、列数、列名，以及前 `preview_rows` 行的数据预览。

- **get_excel_info** `(file_path, include_preview=False, preview_rows=3) -> dict`  
  返回整个文件的信息：路径、大小、工作表数量与名称、各表的行数/列数/列名；`include_preview=True` 时附带每表前几行预览。

---

## Word 模块 (word)

- **read_docx** `(file_path) -> str`  
  读取 Word 文档正文，段落之间用换行符连接，返回纯文本。

- **write_docx** `(content, file_path, title=None) -> None`  
  创建新 Word 文档并写入文本。`title` 可选，会作为文档标题插入。

---

## TXT/文本 模块 (txt)

- **read_txt** `(file_path, encoding="utf-8") -> str`  
  读取纯文本文件全文。适用于 txt、md、py、js 等任意可按文本打开的文件；`encoding` 指定文件编码。

- **write_txt** `(content, file_path, encoding="utf-8") -> None`  
  将文本写入文件，已存在则覆盖。`content` 必须为 str；`encoding` 指定写入编码。

---

## SQLite 模块 (sqlite)

- **query** `(db_path, sql, params=None) -> pd.DataFrame`  
  执行 SQL 查询，返回 DataFrame。`params` 可为 tuple（配合 `?` 占位）或 dict（配合 `:name` 占位），用于参数化查询。

- **get_schema** `(db_path, table_name) -> dict[str, str]`  
  返回指定表的列名到列类型的映射（如 `{'id': 'INTEGER', 'name': 'TEXT'}`）。

- **get_tables** `(db_path) -> list[str]`  
  返回数据库中所有用户表名列表，不含 `sqlite_` 开头的系统表。

- **get_database_info** `(db_path, include_preview=False, preview_rows=3) -> dict`  
  返回数据库概览：路径、大小、表数量与表名、各表的行数/列数/列名/列类型；`include_preview=True` 时附带每表前几行数据。

---

## PDF 模块 (pdf)

- **extract_text** `(file_path, page_range=None) -> str`  
  从 PDF 提取文本。`page_range` 为 `(start, end)`，1-based；`None` 表示全部页面。页面之间用换行分隔。

- **extract_tables** `(file_path, page_range=None) -> list[pd.DataFrame]`  
  从 PDF 提取表格，返回 DataFrame 列表。当前基于 pypdf 的 MVP 实现，合并单元格、复杂布局等可能识别不准。

---

## 异常类 (exceptions)

- **UnifilesError** — 本库所有自定义异常的基类。
- **FileFormatError** — 文件格式不符合预期或无法识别时抛出。
- **FileReadError** — 读取文件时发生错误时抛出。
- **FileWriteError** — 写入文件时发生错误时抛出。

## 使用示例

```python
from unifiles import (
    read_excel,
    write_excel,
    get_sheet_names,
    read_docx,
    write_docx,
    read_txt,
    write_txt,
    query,
    get_tables,
    extract_text,
    extract_tables,
    FileReadError,
)

# Excel
df = read_excel("data.xlsx", sheet_name=0)
sheets = get_sheet_names("data.xlsx")

# Word
text = read_docx("doc.docx")
write_docx("Hello", "out.docx", title="Title")

# TXT
text = read_txt("readme.md")
write_txt("content", "out.txt", encoding="utf-8")

# SQLite
tables = get_tables("app.db")
result = query("app.db", "SELECT * FROM users WHERE id = ?", (1,))

# PDF
full_text = extract_text("doc.pdf")
tables = extract_tables("doc.pdf", page_range=(1, 5))
```

更详细的参数、返回值与异常说明请参考各函数在源码中的 docstring。

---
