# 代码规范 (Code Style Guide)

> 本文件定义 unifiles 项目的代码风格标准。

## 类型注解（Python 3.10+ 现代语法）

```python
# ✅ 使用内置类型和 | 联合运算符
def read(file_path: str, sheet: str | int | None = None) -> pd.DataFrame: ...
def process(items: list[str]) -> dict[str, int]: ...

# ❌ 禁止旧式 typing 导入
from typing import List, Dict, Union, Optional  # 禁止
```

## 导入顺序（组间空行）

```python
# 1. 标准库
from pathlib import Path

# 2. 第三方库
import pandas as pd

# 3. 本地（相对导入）
from .exceptions import FileReadError
```

## Docstring（Google 风格，中文）

```python
def read_excel(file_path: str, sheet_name: str | None = None) -> pd.DataFrame:
    """读取 Excel 文件内容。

    Args:
        file_path: Excel 文件路径
        sheet_name: 工作表名称，None 表示第一个工作表

    Returns:
        包含 Excel 数据的 DataFrame

    Raises:
        FileNotFoundError: 文件不存在

    Example:
        >>> df = read_excel("data.xlsx")
    """
```

## 错误处理

```python
# 1. 检查文件存在性
path = Path(file_path)
if not path.exists():
    raise FileNotFoundError(f"文件不存在: {file_path}")

# 2. try/except 带异常链
try:
    return pd.read_excel(file_path, sheet_name=sheet_name)
except FileNotFoundError:
    raise  # 已知异常直接抛出
except Exception as e:
    raise FileReadError(f"读取 Excel 失败: {e}") from e  # 包装并保留异常链
```

**自定义异常**: `UnifilesError`（基类）→ `FileFormatError`、`FileReadError`、`FileWriteError`

## 命名规范

- 函数/变量: `snake_case`（`read_excel`、`file_path`）
- 私有辅助: `_prefix`（`_df_preview_to_records`）
- 常量: `UPPER_SNAKE_CASE`

## 测试规范

```python
import pytest
import pandas as pd
from pathlib import Path
from unifiles.excel import read_excel

def test_read_excel_success(tmp_path: Path):
    """测试成功读取 Excel 文件。"""
    test_file = tmp_path / "test.xlsx"
    df = pd.DataFrame({"A": [1, 2, 3]})
    df.to_excel(test_file, index=False)
    
    result = read_excel(str(test_file))
    assert isinstance(result, pd.DataFrame)
    pd.testing.assert_frame_equal(result, df)

def test_read_excel_not_found():
    """测试文件不存在的情况。"""
    with pytest.raises(FileNotFoundError, match="文件不存在"):
        read_excel("nonexistent.xlsx")
```

**模式**:
- 使用 `tmp_path` fixture 创建临时文件
- `pytest.raises` 带 `match` 验证异常消息
- DataFrame 比较用 `pd.testing.assert_frame_equal`

## API 设计规则

- 所有读取函数: 第一个参数为 `file_path: str`
- 返回值: `DataFrame`（表格）、`str`（文本）、`list`（名称/结构）、`dict`（元数据）
- 所有公共函数必须在 `__init__.py` 中导出
