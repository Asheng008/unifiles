"""废弃函数警告测试。"""

import warnings
from pathlib import Path

from docx import Document

from unifiles.word import read_docx


def test_read_docx_deprecated(tmp_path: Path):
    """测试 read_docx 发出废弃警告。"""
    test_file = tmp_path / "test.docx"
    doc = Document()
    doc.add_paragraph("测试")
    doc.save(test_file)

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = read_docx(str(test_file))
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "已废弃" in str(w[0].message)
