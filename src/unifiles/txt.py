"""纯文本文件操作模块。

提供 txt、md、代码等纯文本文件的读取和写入功能。
"""

from pathlib import Path
from typing import Any

from .exceptions import FileReadError, FileWriteError


def read_txt(file_path: str, encoding: str = "utf-8") -> str:
    """读取纯文本文件内容。

    适用于 txt、md、py、js 等任意可按文本打开的文件，不按扩展名区分。

    Args:
        file_path: 文本文件路径
        encoding: 文件编码，默认 utf-8。常见如 "gbk"（部分 Windows 中文文本）、"utf-8" 等。

    Returns:
        文件全文内容

    Raises:
        FileNotFoundError: 文件不存在
        FileReadError: 读取文件时发生错误

    Example:
        >>> content = read_txt("readme.md")
        >>> code = read_txt("main.py", encoding="utf-8")
        >>> # Windows 下部分中文 txt 为 GBK 编码时可指定：
        >>> content = read_txt("legacy.txt", encoding="gbk")
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    try:
        return path.read_text(encoding=encoding)
    except FileNotFoundError:
        raise
    except UnicodeDecodeError as e:
        hint = (
            "若文件为 GBK 等编码，可尝试传入 encoding='gbk'"
            if encoding == "utf-8"
            else ""
        )
        raise FileReadError(f"读取文本文件失败（解码错误）: {e}. {hint}".strip()) from e
    except Exception as e:
        raise FileReadError(f"读取文本文件失败: {e}") from e


def write_txt(content: Any, file_path: str, encoding: str = "utf-8") -> None:
    """将内容写入纯文本文件。

    若目标文件已存在则覆盖。适用于 txt、md、代码等任意纯文本输出。

    Args:
        content: 要写入的文本内容（须为 str，否则抛出 ValueError）
        file_path: 输出文件路径
        encoding: 写入使用的编码，默认 utf-8；如需与旧版 Windows 兼容可传 "gbk" 等。

    Raises:
        ValueError: 内容格式无效（非 str）
        PermissionError: 文件权限不足
        FileWriteError: 写入文件时发生错误

    Example:
        >>> write_txt("Hello World", "out.txt")
        >>> write_txt("# Title\\n\\nBody", "doc.md", encoding="utf-8")
    """
    if not isinstance(content, str):
        raise ValueError(f"内容格式无效，期望 str，实际类型: {type(content)}")

    path = Path(file_path)
    try:
        path.write_text(content, encoding=encoding)
    except PermissionError:
        raise
    except Exception as e:
        raise FileWriteError(f"写入文本文件失败: {e}") from e
