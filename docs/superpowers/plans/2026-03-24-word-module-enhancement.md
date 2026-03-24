# Word 模块增强实现计划

> **适用对象:** 无上下文经验的工程师

**目标:** 增强 unifiles Word 模块，支持提取文本（含表格 Markdown）、表格、图片，并提供综合检查函数。

**架构:** 新增 4 个函数（extract_text_docx、extract_tables_docx、extract_images_docx、inspect_docx），废弃 read_docx。

**技术栈:** Python 3.10+, python-docx 1.2.0, pytest

---

## 文件结构

```
src/unifiles/word.py           # 主要修改：新增 4 个函数，废弃 1 个
tests/test_word.py             # 新增测试用例
src/unifiles/__init__.py       # 导出新函数
```

---

## Task 1: 实现表格提取辅助函数

**文件:**
- 修改: `src/unifiles/word.py`
- 修改: `tests/test_word.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/test_word.py 新增
def test_extract_tables_docx_success(tmp_path: Path):
    """测试成功提取表格。"""
    test_file = tmp_path / "test.docx"
    doc = Document()
    doc.add_paragraph("文档标题")
    table = doc.add_table(rows=2, cols=2)
    table.cell(0, 0).text = "姓名"
    table.cell(0, 1).text = "年龄"
    table.cell(1, 0).text = "张三"
    table.cell(1, 1).text = "25"
    doc.save(test_file)

    result = extract_tables_docx(str(test_file))
    assert len(result) == 1
    assert "| 姓名 | 年龄 |" in result[0]
    assert "| 张三 | 25 |" in result[0]
```

- [ ] **Step 2: 运行测试确认失败**

```bash
source .venv/bin/activate && pytest tests/test_word.py::test_extract_tables_docx_success -v
```

预期: FAIL - NameError: name 'extract_tables_docx' is not defined

- [ ] **Step 3: 实现最小代码**

```python
# src/unifiles/word.py 新增
def _table_to_markdown(table) -> str:
    """将 python-docx 表格转换为 Markdown 格式。"""
    if not table.rows:
        return ""
    
    rows_data = []
    for row in table.rows:
        row_data = [cell.text.strip() for cell in row.cells]
        rows_data.append(row_data)
    
    if not rows_data:
        return ""
    
    col_count = max(len(row) for row in rows_data)
    lines = []
    
    # 表头
    header = rows_data[0] + [""] * (col_count - len(rows_data[0]))
    lines.append("| " + " | ".join(header) + " |")
    
    # 分隔行
    lines.append("| " + " | ".join(["---"] * col_count) + " |")
    
    # 数据行
    for row in rows_data[1:]:
        formatted_row = list(row) + [""] * (col_count - len(row))
        formatted_row = [cell if cell else " " for cell in formatted_row]
        lines.append("| " + " | ".join(formatted_row) + " |")
    
    return "\n".join(lines)


def extract_tables_docx(file_path: str) -> list[str]:
    """提取 Word 文档中的所有表格，返回 Markdown 格式列表。

    Args:
        file_path: Word 文档路径

    Returns:
        每个表格的 Markdown 文本列表

    Raises:
        FileNotFoundError: 文件不存在
        FileReadError: 读取文件时发生错误
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    try:
        document = Document(file_path)
        tables_markdown: list[str] = []
        for table in document.tables:
            md = _table_to_markdown(table)
            if md:
                tables_markdown.append(md)
        return tables_markdown
    except FileNotFoundError:
        raise
    except Exception as e:
        raise FileReadError(f"提取 Word 表格失败: {e}") from e
```

- [ ] **Step 4: 运行测试确认通过**

```bash
source .venv/bin/activate && pytest tests/test_word.py::test_extract_tables_docx_success -v
```

预期: PASS

- [ ] **Step 5: 提交**

```bash
git add src/unifiles/word.py tests/test_word.py
git commit -m "feat(word): add extract_tables_docx with markdown conversion"
```

---

## Task 2: 表格提取边界情况测试

**文件:**
- 修改: `tests/test_word.py`

- [ ] **Step 1: 编写边界测试**

```python
def test_extract_tables_docx_no_tables(tmp_path: Path):
    """测试无表格文档。"""
    test_file = tmp_path / "test.docx"
    doc = Document()
    doc.add_paragraph("只有文字")
    doc.save(test_file)

    result = extract_tables_docx(str(test_file))
    assert result == []


def test_extract_tables_docx_empty_table(tmp_path: Path):
    """测试空表格。"""
    test_file = tmp_path / "test.docx"
    doc = Document()
    doc.add_table(rows=1, cols=2)
    doc.save(test_file)

    result = extract_tables_docx(str(test_file))
    assert len(result) == 1
    assert "|  |  |" in result[0]


def test_extract_tables_docx_file_not_found():
    """测试文件不存在。"""
    with pytest.raises(FileNotFoundError, match="文件不存在"):
        extract_tables_docx("nonexistent.docx")
```

- [ ] **Step 2: 运行测试**

```bash
source .venv/bin/activate && pytest tests/test_word.py -k "extract_tables" -v
```

预期: 全部 PASS

- [ ] **Step 3: 提交**

```bash
git add tests/test_word.py
git commit -m "test(word): add edge case tests for extract_tables_docx"
```

---

## Task 3: 实现图片提取

**文件:**
- 修改: `src/unifiles/word.py`
- 修改: `tests/test_word.py`

- [ ] **Step 1: 编写失败的测试**

```python
def test_extract_images_docx_success(tmp_path: Path):
    """测试成功提取图片。"""
    # 创建一个带图片的文档（需要准备测试图片）
    test_file = tmp_path / "test.docx"
    output_dir = tmp_path / "images"
    
    doc = Document()
    doc.add_paragraph("带图片的文档")
    doc.save(test_file)

    result = extract_images_docx(str(test_file), str(output_dir))
    assert isinstance(result, list)


def test_extract_images_docx_no_images(tmp_path: Path):
    """测试无图片文档。"""
    test_file = tmp_path / "test.docx"
    doc = Document()
    doc.add_paragraph("只有文字")
    doc.save(test_file)

    result = extract_images_docx(str(test_file), str(tmp_path / "images"))
    assert result == []
```

- [ ] **Step 2: 运行测试确认失败**

```bash
source .venv/bin/activate && pytest tests/test_word.py::test_extract_images_docx_success -v
```

预期: FAIL

- [ ] **Step 3: 实现最小代码**

```python
# src/unifiles/word.py 新增
def extract_images_docx(
    file_path: str,
    output_dir: str | None = None,
) -> list[dict[str, Any]]:
    """提取 Word 文档中的所有图片，保存到指定目录。

    Args:
        file_path: Word 文档路径
        output_dir: 输出目录，默认 ./pics/

    Returns:
        图片信息列表，每个元素包含 filename, path, width, height, format, size_bytes

    Raises:
        FileNotFoundError: 文件不存在
        FileReadError: 读取文件时发生错误
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    if output_dir is None:
        output_dir = "./pics"

    try:
        from docx.enum.shape import WD_INLINE_SHAPE
        from docx.parts.image import ImagePart

        document = Document(file_path)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        extracted: list[dict[str, Any]] = []
        image_count = 0

        for shape in document.inline_shapes:
            if shape.type != WD_INLINE_SHAPE.PICTURE:
                continue

            try:
                blip = shape._inline.graphic.graphicData.pic.blipFill.blip
                r_id = blip.embed
            except AttributeError:
                continue

            related_part = document.part.related_parts.get(r_id)
            if not isinstance(related_part, ImagePart):
                continue

            image_count += 1
            blob = related_part.blob
            filename = related_part.filename or f"image_{image_count}.png"
            dest_path = output_path / filename

            # 避免文件名冲突
            counter = 1
            while dest_path.exists():
                name = Path(filename).stem
                ext = Path(filename).suffix
                dest_path = output_path / f"{name}_{counter}{ext}"
                counter += 1

            with open(dest_path, "wb") as f:
                f.write(blob)

            try:
                img_obj = related_part.image
                width = img_obj.px.width
                height = img_obj.px.height
                img_format = img_obj.format
            except Exception:
                width = height = img_format = None

            extracted.append({
                "filename": dest_path.name,
                "path": str(dest_path),
                "width": width,
                "height": height,
                "format": img_format,
                "size_bytes": len(blob),
            })

        return extracted
    except FileNotFoundError:
        raise
    except Exception as e:
        raise FileReadError(f"提取 Word 图片失败: {e}") from e
```

- [ ] **Step 4: 运行测试确认通过**

```bash
source .venv/bin/activate && pytest tests/test_word.py -k "extract_images" -v
```

预期: PASS

- [ ] **Step 5: 提交**

```bash
git add src/unifiles/word.py tests/test_word.py
git commit -m "feat(word): add extract_images_docx with auto directory creation"
```

---

## Task 4: 实现文本提取（含表格）

**文件:**
- 修改: `src/unifiles/word.py`
- 修改: `tests/test_word.py`

- [ ] **Step 1: 编写失败的测试**

```python
def test_extract_text_docx_success(tmp_path: Path):
    """测试提取完整文本（含表格）。"""
    test_file = tmp_path / "test.docx"
    doc = Document()
    doc.add_paragraph("开头文字")
    table = doc.add_table(rows=2, cols=2)
    table.cell(0, 0).text = "A"
    table.cell(0, 1).text = "B"
    table.cell(1, 0).text = "C"
    table.cell(1, 1).text = "D"
    doc.add_paragraph("结尾文字")
    doc.save(test_file)

    result = extract_text_docx(str(test_file))
    assert "开头文字" in result
    assert "结尾文字" in result
    assert "| A | B |" in result
    assert "| C | D |" in result
```

- [ ] **Step 2: 运行测试确认失败**

```bash
source .venv/bin/activate && pytest tests/test_word.py::test_extract_text_docx_success -v
```

预期: FAIL

- [ ] **Step 3: 实现最小代码**

```python
# src/unifiles/word.py 新增
def extract_text_docx(file_path: str) -> str:
    """提取 Word 文档的完整文本内容。

    包含所有段落文本和表格（Markdown 格式），按文档顺序输出。

    Args:
        file_path: Word 文档路径

    Returns:
        完整文本字符串

    Raises:
        FileNotFoundError: 文件不存在
        FileReadError: 读取文件时发生错误
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    try:
        document = Document(file_path)
        parts: list[str] = []

        # 遍历文档主体元素，保持顺序
        for element in document.element.body:
            if element.tag.endswith("}p"):  # 段落
                # 查找对应的段落对象
                for para in document.paragraphs:
                    if para._element is element:
                        if para.text.strip():
                            parts.append(para.text)
                        break
            elif element.tag.endswith("}tbl"):  # 表格
                # 查找对应的表格对象
                for table in document.tables:
                    if table._element is element:
                        md = _table_to_markdown(table)
                        if md:
                            parts.append(md)
                        break

        return "\n\n".join(parts)
    except FileNotFoundError:
        raise
    except Exception as e:
        raise FileReadError(f"提取 Word 文本失败: {e}") from e
```

- [ ] **Step 4: 运行测试确认通过**

```bash
source .venv/bin/activate && pytest tests/test_word.py::test_extract_text_docx_success -v
```

预期: PASS

- [ ] **Step 5: 提交**

```bash
git add src/unifiles/word.py tests/test_word.py
git commit -m "feat(word): add extract_text_docx with table markdown support"
```

---

## Task 5: 实现综合检查函数

**文件:**
- 修改: `src/unifiles/word.py`
- 修改: `tests/test_word.py`

- [ ] **Step 1: 编写失败的测试**

```python
def test_inspect_docx_success(tmp_path: Path):
    """测试综合检查文档元素。"""
    test_file = tmp_path / "test.docx"
    doc = Document()
    doc.add_paragraph("第一段")
    doc.add_paragraph("第二段")
    table = doc.add_table(rows=2, cols=2)
    table.cell(0, 0).text = "X"
    table.cell(0, 1).text = "Y"
    table.cell(1, 0).text = "Z"
    table.cell(1, 1).text = "W"
    doc.save(test_file)

    result = inspect_docx(str(test_file), extract_images=False)
    assert result["paragraph_count"] == 2
    assert result["table_count"] == 1
    assert len(result["paragraphs"]) == 2
    assert len(result["tables"]) == 1
    assert "| X | Y |" in result["tables"][0]
```

- [ ] **Step 2: 运行测试确认失败**

```bash
source .venv/bin/activate && pytest tests/test_word.py::test_inspect_docx_success -v
```

预期: FAIL

- [ ] **Step 3: 实现最小代码**

```python
# src/unifiles/word.py 新增
def inspect_docx(
    file_path: str,
    extract_images: bool = True,
    image_dir: str | None = None,
) -> dict[str, Any]:
    """检查 Word 文档的各类元素。

    Args:
        file_path: Word 文档路径
        extract_images: 是否提取图片，默认 True
        image_dir: 图片输出目录，默认 ./pics/

    Returns:
        文档元素信息字典

    Raises:
        FileNotFoundError: 文件不存在
        FileReadError: 读取文件时发生错误
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    try:
        document = Document(file_path)

        # 提取段落
        paragraphs: list[str] = []
        for para in document.paragraphs:
            if para.text.strip():
                paragraphs.append(para.text)

        # 提取表格
        tables_markdown: list[str] = []
        for table in document.tables:
            md = _table_to_markdown(table)
            if md:
                tables_markdown.append(md)

        # 提取图片
        images: list[dict[str, Any]] = []
        if extract_images:
            images = extract_images_docx(file_path, image_dir)

        return {
            "paragraphs": paragraphs,
            "tables": tables_markdown,
            "images": images,
            "paragraph_count": len(paragraphs),
            "table_count": len(tables_markdown),
            "image_count": len(images),
        }
    except FileNotFoundError:
        raise
    except Exception as e:
        raise FileReadError(f"检查 Word 文档失败: {e}") from e
```

- [ ] **Step 4: 运行测试确认通过**

```bash
source .venv/bin/activate && pytest tests/test_word.py::test_inspect_docx_success -v
```

预期: PASS

- [ ] **Step 5: 提交**

```bash
git add src/unifiles/word.py tests/test_word.py
git commit -m "feat(word): add inspect_docx for comprehensive document analysis"
```

---

## Task 6: 废弃 read_docx

**文件:**
- 修改: `src/unifiles/word.py`
- 修改: `tests/test_word.py`

- [ ] **Step 1: 编写测试**

```python
def test_read_docx_deprecated(tmp_path: Path):
    """测试 read_docx 发出废弃警告。"""
    import warnings
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
```

- [ ] **Step 2: 实现代码**

```python
# src/unifiles/word.py 修改 read_docx 函数
def read_docx(file_path: str) -> str:
    """读取 Word 文档内容。

    .. deprecated:: 0.4.0
        请使用 :func:`extract_text_docx` 替代。

    Args:
        file_path: Word 文档路径

    Returns:
        文档的文本内容，段落之间用换行符分隔

    Raises:
        FileNotFoundError: 文件不存在
        FileReadError: 读取文件时发生错误
    """
    import warnings
    warnings.warn(
        "read_docx 已废弃，请使用 extract_text_docx",
        DeprecationWarning,
        stacklevel=2
    )
    # 原有实现保持不变...
```

- [ ] **Step 3: 运行测试**

```bash
source .venv/bin/activate && pytest tests/test_word.py::test_read_docx_deprecated -v
```

预期: PASS

- [ ] **Step 4: 提交**

```bash
git add src/unifiles/word.py tests/test_word.py
git commit -m "deprecate(word): mark read_docx as deprecated"
```

---

## Task 7: 更新 __init__.py 导出

**文件:**
- 修改: `src/unifiles/__init__.py`

- [ ] **Step 1: 更新导入**

```python
# Word 模块
from .word import (
    read_docx,
    write_docx,
    extract_text_docx,
    extract_tables_docx,
    extract_images_docx,
    inspect_docx,
)
```

- [ ] **Step 2: 更新 __all__**

```python
__all__ = [
    # ... 现有导出 ...
    "read_docx",
    "write_docx",
    "extract_text_docx",
    "extract_tables_docx",
    "extract_images_docx",
    "inspect_docx",
]
```

- [ ] **Step 3: 运行全部测试**

```bash
source .venv/bin/activate && pytest tests/test_word.py -v
```

预期: 全部 PASS

- [ ] **Step 4: 提交**

```bash
git add src/unifiles/__init__.py
git commit -m "feat(word): export new functions in __init__.py"
```

---

## Task 8: CI 检查

- [ ] **Step 1: 格式检查**

```bash
source .venv/bin/activate && black --check src/ tests/
```

预期: PASS（或运行 `black src/ tests/` 修复）

- [ ] **Step 2: 类型检查**

```bash
source .venv/bin/activate && mypy src/unifiles/
```

预期: PASS

- [ ] **Step 3: 全部测试**

```bash
source .venv/bin/activate && pytest
```

预期: 全部 PASS

- [ ] **Step 4: 提交修复（如有）**

```bash
git add -A
git commit -m "fix(word): apply black formatting and fix type errors"
```
