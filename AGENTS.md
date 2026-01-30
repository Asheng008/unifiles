# AGENTS.md - Project Context & Directives

> **SYSTEM NOTICE**: 此文件是本项目最高优先级的上下文文档。所有 AI Agent (Cursor, Windsurf, Copilot 等) 在执行任务前必须阅读并遵守以下规范。

## 1. 项目概述 (Project Overview)

- **角色定位**: 高级 Python 软件工程师，专注于文件操作工具库开发。
- **核心专长**: 统一的文件操作接口，支持多种文件类型的读取、写入、抽取和查询。
- **技术栈**: Python 3.10+，严格类型注解（使用 Python 3.10+ 现代语法），遵循 SOLID 原则和清洁架构。
- **目标**: 构建高效、可维护、类型安全的文件操作工具函数库。

## 2. 系统运行环境 (Environment Context)

> **CRITICAL**: 当前宿主环境为 **Windows 11**，默认 Shell 为 **PowerShell**。

- **OS**: Windows 11
- **Shell**: PowerShell 5.1 / 7+
- **路径规范**:
  - 代码中 (Python): 始终使用正斜杠 `/` 或 `pathlib.Path`。
  - 终端命令中: 注意反斜杠 `\` 的兼容性。
- **命令行约束**:
  - ❌ **严禁**使用 Linux 专属命令: `export`, `ls -la`, `touch`, `rm -rf`, `source`。
  - ✅ **必须**使用 PowerShell 语法:
    - 设置变量: `$env:VAR='val'`
    - 激活环境: `.\.venv\Scripts\Activate.ps1`
    - 文件操作: `New-Item`, `Remove-Item`, `Get-Content`
    - 链式命令: 使用 `;` 分隔。
  - ✅ **Python 命令执行**: 执行任何 Python 命令前，**必须**先激活当前项目的虚拟环境:
    - 激活虚拟环境: `.\.venv\Scripts\Activate.ps1`
    - 或在命令链中激活: `.\.venv\Scripts\Activate.ps1; python <script.py>`
    - 或使用完整路径: `.\.venv\Scripts\python.exe <script.py>`
    - **严禁**直接使用系统 Python (`python`)，必须使用虚拟环境中的 Python
  - ✅ **编码设置**: 执行终端命令前，**必须**先设置 UTF-8 编码以防止中文输出乱码:
    - 优先使用: `chcp 65001` (设置代码页为 UTF-8)
    - 备选方案: PowerShell 5+ 可使用 `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`
    - 建议在命令链开头执行: `chcp 65001; <your-command>`

## 3. 工具体系与调用策略 (Tools & Strategy)

你拥有强大的 MCP 工具集。若特定名称工具（如 Context7）不可用，请使用下一个优先级工具。

### 3.1 核心工具链 (按优先级排序)

1.  **Context7** - **[最高优先级]**
    - **用途**: 获取**指定库的最新官方文档**和**项目现有代码**。
    - **规则**: 写代码前，**必须**先查阅相关库的最新文档（pandas, openpyxl, pypdf, python-docx）。
    - **指令**: "查询 pandas read_excel 最新用法", "查询 python-docx 文档操作示例", "读取 excel.py 查看当前实现"。

2.  **RefTool** - **[知识补充]**
    - **用途**: 搜索通用技术文档或验证 API 签名。
    - **规则**: 当 Context7 未覆盖（如第三方库用法、最佳实践）时使用。
    - **示例**: 搜索 "pandas ExcelWriter 多工作表写入", "pypdf 表格提取方法"。

3.  **DeepWiki** - **[架构理解]**
    - **用途**: 读取 GitHub 仓库结构或大型文档库。
    - **规则**: 引入新模块或重构项目结构时使用。
    - **示例**: 查看 pandas、openpyxl 等库的 GitHub 仓库结构。

4.  **Web Access (网络搜索)** - **[最后兜底]**
    - **用途**: 解决具体报错 (StackOverflow) 或查找最新博客教程。
    - **规则**: 当前面工具无法解决问题时使用。

## 4. 开发规范与最佳实践 (Development Standards)

### 4.1 代码规范
- **类型安全**: 所有函数参数**必须**有类型提示（Type Hints）。
- **类型注解风格**: 使用 **Python 3.10+ 现代语法**：
  - ✅ 使用 `list[str]` 而不是 `List[str]`
  - ✅ 使用 `dict[str, int]` 而不是 `Dict[str, int]`
  - ✅ 使用 `tuple[int, int]` 而不是 `Tuple[int, int]`
  - ✅ 使用 `str | int | None` 而不是 `Union[str, int, None]` (Python 3.10+)
  - ✅ 优先使用内置类型，避免从 `typing` 导入（除非必需）
- **文档字符串**: 所有公共函数**必须**提供 Google 风格的 docstring。
- **错误处理**: 使用 Python 标准异常（FileNotFoundError, ValueError等），提供清晰的错误信息。
- **代码风格**: 遵循 PEP 8 规范，使用 4 个空格缩进。

### 4.2 API 设计原则
- **一致性**: 所有读取函数统一使用 `file_path` 作为第一个参数。
- **返回值**: DataFrame 用于表格数据，str 用于文本数据，list 用于列表数据。
- **参数命名**: 使用清晰、描述性的参数名，避免缩写。
- **路径处理**: 优先使用 `pathlib.Path` 进行路径操作，提高跨平台兼容性。

### 4.3 Python 版本与类型注解规范

#### Python 版本要求
- **最低版本**: Python 3.10+
- **推荐版本**: Python 3.11+（可选，用于最新特性）

#### 类型注解最佳实践（Python 3.10+）
```python
# ✅ 推荐：使用内置类型（Python 3.10+）
def process_data(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# ✅ 推荐：使用联合类型运算符（Python 3.10+，优先使用）
def read_file(file_path: str | Path) -> str | None:
    ...

# ⚠️ 兼容：若需支持 Python 3.10 以下，可使用 Union
from typing import Union
def read_file(file_path: Union[str, Path]) -> Union[str, None]:  # 旧版 Python 兼容
    ...

# ❌ 避免：旧式类型注解（Python 3.9 及以下）
from typing import List, Dict, Union, Optional
def process_data(items: List[str]) -> Dict[str, int]:  # 不推荐
    ...
```

**注意**: 项目要求 Python 3.10+，使用内置类型与 `|` 联合类型语法，代码简洁现代。

#### 类型注解检查
- 使用 `mypy` 进行类型检查：`mypy src/unifiles/`
- 配置 `pyproject.toml` 中的 `[tool.mypy]` 部分
- 确保所有公共函数都有完整的类型注解

### 4.4 依赖库使用规范
- **pandas**: 用于 Excel 和 SQLite 的数据处理，返回 DataFrame。
- **openpyxl**: 用于 Excel 文件的底层操作（如获取工作表名称）。
- **pypdf**: 用于 PDF 的文本提取与**基础表格提取**；复杂布局、多列、合并单元格等场景识别有限，后续可考虑引入 **pdfplumber** 提升表格效果。
- **python-docx**: 用于 Word 文档的读写操作。
- **sqlite3**: Python 标准库，用于 SQLite 数据库操作。

### 4.5 错误处理规范
- **文件不存在**: 使用 `FileNotFoundError`，提供完整的文件路径信息。
- **格式错误**: 使用 `ValueError`，说明具体的格式问题。
- **权限问题**: 使用 `PermissionError`，说明具体的权限问题。
- **其他错误**: 使用自定义异常类（`unifiles.exceptions`），保持异常链（`from e`）。


## 5. 项目结构规范 (Project Structure)

### 5.1 目录结构
```
unifiles/
├── pyproject.toml          # 项目配置和依赖管理
├── README.md               # 项目说明文档
├── src/
    └── unifiles/
        ├── __init__.py     # 包初始化，导出主要API
        ├── excel.py        # Excel文件操作模块
        ├── pdf.py          # PDF文件操作模块
        ├── word.py         # Word文档操作模块
        ├── sqlite.py       # SQLite数据库操作模块
        └── exceptions.py   # 自定义异常类
└── tests/                  # 测试代码
    ├── __init__.py
    ├── test_excel.py
    ├── test_pdf.py
    ├── test_word.py
    ├── test_sqlite.py
    └── fixtures/           # 测试用的示例文件
        └── test_files/
```

### 5.2 模块设计原则
- **单一职责**: 每个模块专注于一种文件类型的操作。
- **独立性**: 模块之间保持低耦合，可以独立导入使用。
- **统一接口**: 相同操作类型的函数保持一致的签名和返回值。

### 5.3 模块导入和导出规范
- **__init__.py**: 必须导出所有公共API函数，方便用户直接使用 `unifiles.read_excel()`。
- **导入方式**: 支持两种导入方式：
  - `import unifiles` 然后使用 `unifiles.read_excel()`
  - `from unifiles import read_excel` 直接导入函数
- **版本信息**: 在 `__init__.py` 中定义 `__version__` 变量。

## 6. 代码风格示例 (Code Style Examples)

### 6.1 函数实现示例 (Implementation)
```python
# excel.py
import pandas as pd
from pathlib import Path

def read_excel(
    file_path: str, 
    sheet_name: str | int | None = None
) -> pd.DataFrame:
    """
    读取Excel文件内容。
    
    Args:
        file_path: Excel文件路径
        sheet_name: 工作表名称或索引，None表示读取第一个工作表
        
    Returns:
        包含Excel数据的DataFrame对象
        
    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 工作表不存在或无效
        
    Example:
        >>> df = read_excel("data.xlsx", sheet_name="Sheet1")
        >>> print(df.head())
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except Exception as e:
        raise ValueError(f"读取Excel文件失败: {e}") from e


def get_sheet_names(file_path: str) -> list[str]:
    """
    获取Excel文件中的所有工作表名称。
    
    Args:
        file_path: Excel文件路径
        
    Returns:
        工作表名称列表
        
    Raises:
        FileNotFoundError: 文件不存在
        
    Example:
        >>> sheets = get_sheet_names("data.xlsx")
        >>> print(sheets)
        ['Sheet1', 'Sheet2']
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    try:
        excel_file = pd.ExcelFile(file_path)
        return excel_file.sheet_names
    except Exception as e:
        raise ValueError(f"获取工作表名称失败: {e}") from e
```

### 6.2 测试代码示例 (Testing)
**必须**编写测试以验证函数逻辑。使用 `pytest`。

```python
# tests/test_excel.py
import pytest
import pandas as pd
from pathlib import Path
from unifiles.excel import read_excel, get_sheet_names

def test_read_excel_success(tmp_path):
    """测试成功读取Excel文件"""
    # 创建测试文件
    test_file = tmp_path / "test.xlsx"
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    df.to_excel(test_file, index=False)
    
    # 测试读取
    result = read_excel(str(test_file))
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3


def test_read_excel_file_not_found():
    """测试文件不存在的情况"""
    with pytest.raises(FileNotFoundError):
        read_excel("nonexistent.xlsx")


def test_get_sheet_names(tmp_path):
    """测试获取工作表名称"""
    test_file = tmp_path / "test.xlsx"
    df = pd.DataFrame({"A": [1, 2, 3]})
    
    # 创建多工作表文件
    with pd.ExcelWriter(test_file) as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)
        df.to_excel(writer, sheet_name="Sheet2", index=False)
    
    sheets = get_sheet_names(str(test_file))
    assert "Sheet1" in sheets
    assert "Sheet2" in sheets
    assert len(sheets) == 2
```

## 7. 操作工作流 (Operational Workflow)

**Step 1: 发现 (Discovery)**
- 🔍 **Action**: 使用 `Context7` 读取现有代码文件（如 `excel.py`）了解当前实现。
- 🧠 **Check**: 确认现有函数命名规范和代码风格。

**Step 2: 需求分析 (Requirements Analysis)**
- 🔍 **Action**: 阅读 `TECH_REQUIREMENTS.md` 了解功能需求。
- 🧠 **Check**: 确认要实现的函数签名、参数类型和返回值。

**Step 3: 文档查阅 (Documentation)**
- 🔍 **Action**: 使用 `Context7` 查询相关库的最新官方文档（pandas, openpyxl, pypdf, python-docx）。
- 📝 **Action**: 如果不确定API用法，使用 `RefTool` 搜索最佳实践。
- 🧠 **Check**: 确保使用最新的API和最佳实践。

**Step 4: 设计规范 (Design Specification)**
- 📝 **Action**: 确定函数签名和参数设计。
- 🧠 **Check**: 确保API设计与现有模块保持一致。

**Step 5: 实现代码 (Implementation)**
- 💻 **Action**: 编写函数实现代码。
- ✅ **Constraint**: 确保类型注解完整，确保错误处理完善，确保docstring完整。

**Step 6: 编写测试 (Testing)**
- 🧪 **Action**: 创建/运行 `tests/` 下的测试用例。
- 👁️ **Check**: 测试正常流程和异常流程，确保代码覆盖率达标。

**Step 7: 更新文档 (Documentation)**
- 📚 **Action**: 更新 `__init__.py` 导出新函数，更新 README.md 使用示例。

## 8. 检查清单 (Pre-Flight Checklist)

在提交代码前，必须在心中打钩：
- [ ] **工具**: 是否先查阅了 Context7/RefTool 获取最新文档？
- [ ] **环境**: 是否使用了 PowerShell 兼容路径和命令？
- [ ] **Python版本**: 代码是否兼容 Python 3.10+？
- [ ] **类型注解**: 是否使用了 Python 3.10+ 现代语法（`list[str]` 而非 `List[str]`）？
- [ ] **类型完整性**: 是否所有函数参数和返回值都有 Type Hint？
- [ ] **文档**: 是否所有公共函数都有完整的 docstring（Google 风格）？
- [ ] **错误处理**: 是否使用了合适的异常类型，错误信息是否清晰？
- [ ] **一致性**: API 设计是否与现有模块保持一致？
- [ ] **测试**: 是否编写了测试用例，覆盖正常流程和异常流程？
- [ ] **导入**: 是否在 `__init__.py` 中正确导出了新函数？

## 9. 禁忌与注意事项 (Negative Constraints)

- ❌ **严禁** 使用 Linux 专属命令（如 `export`, `ls -la`, `touch`, `rm -rf`）。
- ❌ **严禁** 假设用户安装了 `make` 或 `bash`。
- ❌ **严禁** 在未阅读现有代码和需求文档的情况下直接添加新功能。
- ❌ **严禁** 使用系统 Python，必须使用项目虚拟环境中的 Python。
- ❌ **严禁** 使用 Python 3.9 及以下的旧式类型注解（如 `List[str]`, `Dict[str, int]`, `Union[str, int]`）。
- ❌ **严禁** 忽略错误处理，所有文件操作必须处理文件不存在、权限不足等异常。
- ❌ **严禁** 硬编码文件路径，必须使用参数传入。
- ❌ **严禁** 修改函数签名而不更新测试用例。
