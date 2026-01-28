"""unifiles - 统一的文件操作库。

提供跨文件类型的统一接口，简化 Python 中对不同类型文件的读取、写入、抽取和查询操作。
"""

__version__ = "0.1.0"

# 导出异常类
from .exceptions import (
    FileFormatError,
    FileReadError,
    FileWriteError,
    UnifilesError,
)

# Excel 模块
from .excel import read_excel, write_excel, get_sheet_names

# 预留后续模块导入位置

# PDF 模块
# from .pdf import extract_text, extract_tables

# Word 模块
# from .word import read_docx, write_docx

# SQLite 模块
# from .sqlite import query, get_schema, get_tables

__all__ = [
    "__version__",
    "UnifilesError",
    "FileFormatError",
    "FileReadError",
    "FileWriteError",
    "read_excel",
    "write_excel",
    "get_sheet_names",
]
