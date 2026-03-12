"""TXT 模块测试用例。"""

import pytest
from pathlib import Path

from unifiles.txt import read_txt, write_txt
from unifiles.exceptions import FileReadError, FileWriteError


def test_read_txt_success(tmp_path: Path):
    """测试成功读取纯文本文件。"""
    test_file = tmp_path / "readme.txt"
    test_file.write_text("第一行\n第二行\n第三行", encoding="utf-8")

    result = read_txt(str(test_file))
    assert isinstance(result, str)
    assert "第一行" in result
    assert "第二行" in result
    assert "第三行" in result
    lines = result.split("\n")
    assert len(lines) == 3


def test_read_txt_multiline_newlines(tmp_path: Path):
    """测试读取含空行与多换行的内容。"""
    test_file = tmp_path / "doc.md"
    content = "line1\n\nline2\n\n\nline3"
    test_file.write_text(content, encoding="utf-8")

    result = read_txt(str(test_file))
    assert result == content
    assert "line1" in result and "line2" in result and "line3" in result


def test_read_txt_file_not_found():
    """测试文件不存在。"""
    with pytest.raises(FileNotFoundError, match="文件不存在"):
        read_txt("nonexistent.txt")


def test_read_txt_encoding(tmp_path: Path):
    """测试指定编码读取。"""
    test_file = tmp_path / "utf8.txt"
    text = "中文内容 English"
    test_file.write_text(text, encoding="utf-8")

    result = read_txt(str(test_file), encoding="utf-8")
    assert result == text


def test_read_txt_other_extensions(tmp_path: Path):
    """测试读取 md、py 等扩展名。"""
    for name in ("readme.md", "main.py", "script.js"):
        f = tmp_path / name
        f.write_text("content", encoding="utf-8")
        assert read_txt(str(f)) == "content"


def test_write_txt_success(tmp_path: Path):
    """测试正常写入。"""
    test_file = tmp_path / "out.txt"
    content = "第一行\n第二行\n第三行"

    write_txt(content, str(test_file))

    assert test_file.exists()
    result = read_txt(str(test_file))
    assert result == content


def test_write_txt_empty_content(tmp_path: Path):
    """测试写入空内容。"""
    test_file = tmp_path / "empty.txt"
    write_txt("", str(test_file))

    assert test_file.exists()
    assert read_txt(str(test_file)) == ""


def test_write_txt_invalid_content(tmp_path: Path):
    """测试无效内容类型。"""
    test_file = tmp_path / "out.txt"

    with pytest.raises(ValueError, match="内容格式无效"):
        write_txt(123, str(test_file))  # type: ignore

    with pytest.raises(ValueError, match="内容格式无效"):
        write_txt(None, str(test_file))  # type: ignore


def test_write_txt_encoding(tmp_path: Path):
    """测试指定编码写入。"""
    test_file = tmp_path / "encoded.txt"
    content = "hello 世界"
    write_txt(content, str(test_file), encoding="utf-8")

    result = read_txt(str(test_file), encoding="utf-8")
    assert result == content


def test_write_txt_to_directory_raises(tmp_path: Path):
    """测试写入目标为目录时抛出异常。"""
    # 传入目录路径作为“文件”路径：Linux 等可能触发 IsADirectoryError -> FileWriteError，Windows 为 PermissionError
    with pytest.raises((FileWriteError, PermissionError)):
        write_txt("x", str(tmp_path))
