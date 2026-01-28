# PDF 模块开发计划（M3）

## 目标
实现 PDF 文件的文本提取和表格提取功能，提供统一的 API 接口。

## 实现内容

### 1. 创建 `src/unifiles/pdf.py` 模块

实现两个核心函数：

#### `extract_text(file_path: str, page_range: tuple[int, int] | None = None) -> str`
- **功能**: 从 PDF 文件中提取文本内容
- **实现方式**:
  - 使用 `from pypdf import PdfReader` 导入
  - 使用 `PdfReader(file_path)` 打开 PDF
  - 如果 `page_range` 为 None，提取所有页面的文本
  - 如果 `page_range` 提供，提取指定范围（start, end）的页面（注意：页面索引从 0 开始，但用户可能期望从 1 开始）
  - 遍历页面，使用 `page.extract_text()` 提取文本
  - 使用换行符连接各页文本
- **页面范围处理**:
  - `page_range` 格式：`(start, end)`，其中 start 和 end 都是 1-based（用户友好）
  - 内部转换为 0-based 索引：`start_page = page_range[0] - 1`, `end_page = page_range[1]`
  - 验证范围有效性：start >= 1, end >= start, end <= 总页数
- **错误处理**:
  - `FileNotFoundError`: 文件不存在时抛出
  - `ValueError`: 页码范围无效或 PDF 文件损坏时抛出
  - `FileReadError`: 读取文件时发生错误时抛出
- **类型注解**: Python 3.9+ 风格（`tuple[int, int] | None`）
- **文档**: Google 风格 docstring，包含 Args、Returns、Raises、Example

#### `extract_tables(file_path: str, page_range: tuple[int, int] | None = None) -> list[pd.DataFrame]`
- **功能**: 从 PDF 文件中提取表格数据
- **实现方式**:
  - **MVP 限制**: pypdf 本身不直接支持表格提取，需要基于文本提取和布局分析
  - **基础实现策略**:
    1. 使用 `page.extract_text(extraction_mode="layout")` 获取布局文本
    2. 尝试识别表格结构（通过分析文本行的对齐和分隔符）
    3. 将识别到的表格转换为 DataFrame
  - **简化实现**（MVP）:
    - 使用 `page.extract_text(extraction_mode="layout")` 提取布局文本
    - 尝试通过正则表达式或简单的分隔符（如制表符、多个空格）识别表格行
    - 将每行分割为列，创建 DataFrame
    - 返回找到的所有表格列表
  - **注意**: 这是一个基础实现，复杂表格（合并单元格、多列布局）可能无法正确识别
- **页面范围处理**: 与 `extract_text` 相同
- **错误处理**:
  - `FileNotFoundError`: 文件不存在时抛出
  - `ValueError`: 页码范围无效或 PDF 文件损坏时抛出
  - `FileReadError`: 读取文件时发生错误时抛出
- **类型注解**: Python 3.9+ 风格
- **文档**: Google 风格 docstring，**必须包含 MVP 限制说明**

### 2. 编写测试文件 `tests/test_pdf.py`

参考 `tests/test_excel.py`、`tests/test_word.py` 和 `tests/test_sqlite.py` 的测试模式，实现以下测试用例：

- `test_extract_text_success(tmp_path)`: 测试正常提取文本
  - 创建简单的 PDF 文件（可以使用 reportlab 或其他库生成）
  - 验证提取的文本内容正确
- `test_extract_text_page_range(tmp_path)`: 测试指定页码范围提取
  - 创建多页 PDF
  - 验证只提取指定范围的页面
- `test_extract_text_page_range_validation(tmp_path)`: 测试页码范围验证
  - 测试无效范围（start > end, start < 1, end > 总页数）
- `test_extract_text_file_not_found()`: 测试文件不存在的情况
  - 验证抛出 `FileNotFoundError`
- `test_extract_text_invalid_pdf(tmp_path)`: 测试无效 PDF 文件
  - 创建非 PDF 文件，验证错误处理
- `test_extract_tables_success(tmp_path)`: 测试基础表格提取
  - 创建包含简单表格的 PDF
  - 验证提取的表格列表和 DataFrame 结构
- `test_extract_tables_page_range(tmp_path)`: 测试指定页码范围提取表格
  - 创建多页 PDF，其中某些页包含表格
  - 验证只提取指定范围的表格
- `test_extract_tables_file_not_found()`: 测试文件不存在的情况
  - 验证抛出 `FileNotFoundError`
- `test_extract_tables_no_tables(tmp_path)`: 测试没有表格的 PDF
  - 验证返回空列表
- `test_extract_tables_complex_layout(tmp_path)`: 测试复杂布局（可选，标记为预期限制）
  - 创建包含复杂表格的 PDF
  - 可以标记为 `pytest.mark.xfail` 或仅记录限制

### 3. 准备测试用的 PDF 文件

在测试中使用 `tmp_path` 动态创建测试 PDF，或准备静态测试文件：
- 简单文本 PDF（用于文本提取测试）
- 包含基础表格的 PDF（用于表格提取测试）
- 复杂布局 PDF（可选，用于测试限制）

**注意**: 可以使用 `reportlab` 或其他库在测试中动态生成 PDF，避免依赖外部文件。

### 4. 更新 `src/unifiles/__init__.py`

- 取消注释 PDF 模块导入：`from .pdf import extract_text, extract_tables`
- 在 `__all__` 列表中添加 `extract_text` 和 `extract_tables`

## 代码风格要求

参考 `src/unifiles/excel.py`、`src/unifiles/word.py` 和 `src/unifiles/sqlite.py` 的实现模式：
- 使用 `pathlib.Path` 进行路径操作
- 文件存在性检查：`path.exists()`
- 异常处理：先检查文件存在性，再捕获具体异常
- 使用自定义异常类：`FileReadError`
- 类型注解使用 Python 3.9+ 现代语法
- 页面索引处理：用户输入使用 1-based，内部转换为 0-based

## 开发步骤

1. **查阅文档**: 确认 pypdf 的标准用法（已完成部分）
2. **实现 extract_text**: 编写文本提取函数，确保页面范围处理正确
3. **实现 extract_tables**: 编写表格提取函数，实现基础表格识别逻辑
4. **编写测试**: 创建 `test_pdf.py`，覆盖正常和异常流程
5. **准备测试文件**: 创建或生成测试用的 PDF 文件
6. **更新导出**: 修改 `__init__.py` 导出新函数
7. **运行测试**: 确保所有测试通过
8. **代码质量检查**: 运行 mypy、black 检查

## 验收标准

- [ ] `pdf.py` 模块实现完成，包含两个函数
- [ ] 所有函数有完整的类型注解（Python 3.9+ 风格）
- [ ] 所有函数有完整的 Google 风格 docstring（包含 MVP 限制说明）
- [ ] 测试覆盖率 >= 80%
- [ ] 所有测试通过（复杂布局测试可标记为预期限制）
- [ ] mypy 类型检查通过
- [ ] black 代码格式化通过
- [ ] `__init__.py` 正确导出新函数

## 技术要点

- **导入**: `from pypdf import PdfReader`
- **文本提取**: 使用 `page.extract_text()` 或 `page.extract_text(extraction_mode="layout")`
- **页面访问**: `reader.pages[index]`（0-based 索引）
- **页面范围**: 用户输入 1-based，内部转换为 0-based
- **表格提取**: MVP 阶段基于布局文本分析，使用简单的分隔符识别
- **pandas 集成**: 返回 `list[pd.DataFrame]`

## 实现细节

### extract_text 函数实现要点

```python
def extract_text(file_path: str, page_range: tuple[int, int] | None = None) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    try:
        reader = PdfReader(file_path)
        total_pages = len(reader.pages)
        
        if page_range is None:
            # 提取所有页面
            start_idx = 0
            end_idx = total_pages
        else:
            start, end = page_range
            # 验证范围
            if start < 1 or end < start or end > total_pages:
                raise ValueError(f"页码范围无效: {page_range}, 总页数: {total_pages}")
            # 转换为 0-based 索引
            start_idx = start - 1
            end_idx = end
        
        # 提取文本
        texts = []
        for i in range(start_idx, end_idx):
            text = reader.pages[i].extract_text()
            texts.append(text)
        
        return "\n".join(texts)
    except FileNotFoundError:
        raise
    except ValueError:
        raise
    except Exception as e:
        raise FileReadError(f"提取 PDF 文本失败: {e}") from e
```

### extract_tables 函数实现要点（MVP 简化版）

```python
def extract_tables(file_path: str, page_range: tuple[int, int] | None = None) -> list[pd.DataFrame]:
    """
    从 PDF 文件中提取表格数据。
    
    **MVP 限制说明**:
    本函数基于 pypdf 的布局文本提取实现，仅支持基础表格提取。
    以下情况可能无法正确识别：
    - 合并单元格的表格
    - 多列布局的复杂表格
    - 嵌套表格
    - 图片中的表格
    
    如需更好的表格提取效果，建议后续版本考虑引入 pdfplumber 等专业库。
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    try:
        reader = PdfReader(file_path)
        total_pages = len(reader.pages)
        
        # 页面范围处理（与 extract_text 相同）
        if page_range is None:
            start_idx = 0
            end_idx = total_pages
        else:
            start, end = page_range
            if start < 1 or end < start or end > total_pages:
                raise ValueError(f"页码范围无效: {page_range}, 总页数: {total_pages}")
            start_idx = start - 1
            end_idx = end
        
        tables: list[pd.DataFrame] = []
        
        # 遍历页面，尝试提取表格
        for i in range(start_idx, end_idx):
            page = reader.pages[i]
            # 使用布局模式提取文本
            layout_text = page.extract_text(extraction_mode="layout")
            
            # 简单的表格识别逻辑（MVP）
            # 尝试通过制表符或连续空格识别表格行
            lines = layout_text.split("\n")
            table_rows = []
            
            for line in lines:
                # 如果行包含制表符或多个连续空格，可能是表格行
                if "\t" in line or "  " in line:
                    # 分割列（优先使用制表符，否则使用多个空格）
                    if "\t" in line:
                        cols = [col.strip() for col in line.split("\t")]
                    else:
                        cols = [col.strip() for col in line.split() if col.strip()]
                    
                    if len(cols) > 1:  # 至少两列才认为是表格
                        table_rows.append(cols)
            
            # 如果找到表格行，创建 DataFrame
            if table_rows:
                # 尝试第一行作为表头
                if len(table_rows) > 1:
                    df = pd.DataFrame(table_rows[1:], columns=table_rows[0])
                else:
                    df = pd.DataFrame(table_rows)
                tables.append(df)
        
        return tables
    except FileNotFoundError:
        raise
    except ValueError:
        raise
    except Exception as e:
        raise FileReadError(f"提取 PDF 表格失败: {e}") from e
```

## 参考文件

- 实现参考: `src/unifiles/excel.py`、`src/unifiles/word.py`、`src/unifiles/sqlite.py`
- 测试参考: `tests/test_excel.py`、`tests/test_word.py`、`tests/test_sqlite.py`
- 异常定义: `src/unifiles/exceptions.py`
- 导出示例: `src/unifiles/__init__.py`

## 注意事项

- **页面索引**: 用户输入使用 1-based（更友好），内部转换为 0-based
- **表格提取限制**: MVP 阶段仅支持基础表格，必须在文档中明确说明限制
- **测试文件**: 可以使用 reportlab 在测试中动态生成 PDF，避免依赖外部文件
- **错误处理**: PDF 文件可能损坏或格式不正确，需要妥善处理异常
- **性能考虑**: 大文件可能需要分页处理，但 MVP 阶段可以简化

## 任务清单

- [ ] 实现 `src/unifiles/pdf.py` 模块
  - [ ] `extract_text` 函数：文本提取，支持页面范围
  - [ ] `extract_tables` 函数：表格提取（MVP 基础实现）
- [ ] 编写 `tests/test_pdf.py` 测试文件
  - [ ] 文本提取测试（正常流程、页面范围、异常）
  - [ ] 表格提取测试（基础表格、页面范围、异常）
- [ ] 准备测试用的 PDF 文件（动态生成或静态文件）
- [ ] 更新 `src/unifiles/__init__.py` 导出函数
- [ ] 运行测试并验证代码质量
