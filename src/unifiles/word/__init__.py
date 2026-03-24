"""Word 文档操作模块。

提供 Word 文档的读取、写入、提取和检查功能。
"""

from ._legacy import read_docx
from .extract import extract_images_docx, extract_tables_docx, extract_text_docx
from .inspect import inspect_docx
from .write import write_docx

__all__ = [
    "read_docx",
    "write_docx",
    "extract_text_docx",
    "extract_tables_docx",
    "extract_images_docx",
    "inspect_docx",
]
