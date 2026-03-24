"""已废弃的 Word 文档读取函数。"""

import warnings
from pathlib import Path

from docx import Document

from ..exceptions import FileReadError


def read_docx(file_path: str) -> str:
    """读取 Word 文档内容。

    .. deprecated::
        已废弃，请使用 :func:`extract_text_docx`。

    Args:
        file_path: Word 文档路径

    Returns:
        文档的文本内容，段落之间用换行符分隔

    Raises:
        FileNotFoundError: 文件不存在
        FileReadError: 读取文件时发生错误
    """
    warnings.warn(
        "read_docx 已废弃，请使用 extract_text_docx",
        DeprecationWarning,
        stacklevel=2,
    )
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    try:
        document = Document(file_path)
        paragraphs_text: list[str] = []
        for para in document.paragraphs:
            if para.text.strip():
                paragraphs_text.append(para.text)
        return "\n".join(paragraphs_text)
    except FileNotFoundError:
        raise
    except Exception as e:
        raise FileReadError(f"读取 Word 文档失败: {e}") from e
