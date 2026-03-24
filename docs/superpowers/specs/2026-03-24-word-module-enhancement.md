# Word 模块增强设计文档

> **日期**: 2026-03-24
> **作者**: Sisyphus (AI Agent)

## 目标

增强 unifiles 的 Word 模块，支持提取文本（含表格 Markdown）、提取表格、提取图片，并提供综合检查函数。

## 现状

当前 `word.py` 只有 `read_docx` 和 `write_docx`，功能过于简单：
- `read_docx`: 只提取段落文本，忽略表格和图片
- `write_docx`: 写入文本，无格式控制

## 新增函数

### 1. `extract_text_docx(file_path: str) -> str`

提取文档完整文本，包含段落和表格（Markdown 格式），按文档顺序输出。

**示例输出：**
```
这是第一段文字

这是第二段文字

| 姓名 | 年龄 |
| --- | --- |
| 张三 | 25 |
| 李四 | 30 |

继续的文字...
```

**参数：**
- `file_path`: Word 文档路径

**返回：**
- 完整文本字符串

**异常：**
- `FileNotFoundError`: 文件不存在
- `FileReadError`: 读取失败

### 2. `extract_tables_docx(file_path: str) -> list[str]`

提取文档中所有表格，返回 Markdown 格式列表。

**返回示例：**
```python
[
    "| 姓名 | 年龄 |\n| --- | --- |\n| 张三 | 25 |",
    "| 产品 | 价格 |\n| --- | --- |\n| A | 100 |"
]
```

**参数：**
- `file_path`: Word 文档路径

**返回：**
- `list[str]`: 每个表格的 Markdown 文本

**异常：**
- `FileNotFoundError`: 文件不存在
- `FileReadError`: 读取失败

### 3. `extract_images_docx(file_path: str, output_dir: str | None = None) -> list[dict[str, Any]]`

提取文档中所有图片，保存到指定目录。

**默认目录：** `./pics/`

**返回示例：**
```python
[
    {
        "filename": "image1.png",
        "path": "./pics/image1.png",
        "width": 800,
        "height": 600,
        "format": "PNG",
        "size_bytes": 12345
    }
]
```

**参数：**
- `file_path`: Word 文档路径
- `output_dir`: 输出目录，默认 `./pics/`

**返回：**
- `list[dict[str, Any]]`: 图片信息列表

**异常：**
- `FileNotFoundError`: 文件不存在
- `FileReadError`: 读取失败

### 4. `inspect_docx(file_path: str, extract_images: bool = True, image_dir: str | None = None) -> dict[str, Any]`

综合检查文档元素，统一入口。

**返回示例：**
```python
{
    "paragraphs": ["第一段", "第二段"],
    "tables": ["| 列1 | 列2 |\n| --- | --- |\n| A | B |"],
    "images": [
        {"filename": "image1.png", "path": "./pics/image1.png", "width": 800, "height": 600, "format": "PNG"}
    ],
    "image_count": 1,
    "table_count": 1,
    "paragraph_count": 2,
}
```

**参数：**
- `file_path`: Word 文档路径
- `extract_images`: 是否提取图片，默认 True
- `image_dir`: 图片输出目录，默认 `./pics/`

**返回：**
- `dict[str, Any]`: 文档元素信息

**异常：**
- `FileNotFoundError`: 文件不存在
- `FileReadError`: 读取失败

### 5. `read_docx` (废弃)

保留原有实现，添加 `DeprecationWarning`：
```python
import warnings
warnings.warn("read_docx 已废弃，请使用 extract_text_docx", DeprecationWarning, stacklevel=2)
```

## 边界情况处理

| 情况 | 处理方式 |
|------|----------|
| 合并单元格 | 正常提取文本，Markdown 格式可能不完美，但数据完整 |
| 空表格/空单元格 | 返回空字符串 |
| 图片目录不存在 | 自动创建 |
| 重复文件名 | 自动添加序号避免覆盖 |
| 无表格/无图片 | 返回空列表，不报错 |

## 技术实现要点

### 表格提取
- 使用 `document.tables` 遍历所有表格
- `table.rows` → `row.cells` → `cell.text` 提取文本
- 处理合并单元格：`cell._tc.grid_span`（水平合并）

### 图片提取
- 使用 `document.inline_shapes` 查找图片
- 检查 `shape.type == WD_INLINE_SHAPE.PICTURE`
- 通过 `doc.part.related_parts[r_id]` 获取图片数据
- `image_part.blob` 获取二进制数据

### 文本提取（含表格）
- 遍历 `document.element.body` 的子元素
- 按顺序处理段落和表格
- 表格转为 Markdown 格式插入

## API 导出

在 `__init__.py` 中添加：
```python
from .word import (
    extract_text_docx,
    extract_tables_docx,
    extract_images_docx,
    inspect_docx,
)
```

## 测试覆盖

- 正常流程：提取文本、表格、图片
- 异常流程：文件不存在、格式错误
- 边界情况：空文档、无表格、无图片、合并单元格
