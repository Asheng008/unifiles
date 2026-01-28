"""Excel 文件操作模块。

提供 Excel 文件的读取、写入和查询功能。
"""

import pandas as pd
from pathlib import Path

from .exceptions import FileReadError, FileWriteError


def read_excel(file_path: str, sheet_name: str | int | None = None) -> pd.DataFrame:
    """读取 Excel 文件内容。

    Args:
        file_path: Excel 文件路径
        sheet_name: 工作表名称或索引，None 表示读取第一个工作表

    Returns:
        包含 Excel 数据的 DataFrame 对象

    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 工作表不存在或无效
        FileReadError: 读取文件时发生错误

    Example:
        >>> df = read_excel("data.xlsx", sheet_name="Sheet1")
        >>> print(df.head())
        >>> # 使用索引读取
        >>> df = read_excel("data.xlsx", sheet_name=0)
        >>> # 读取第一个工作表
        >>> df = read_excel("data.xlsx")
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    try:
        result = pd.read_excel(file_path, sheet_name=sheet_name)
        # 如果 sheet_name=None 且返回的是字典（只有一个工作表时也可能返回字典），提取第一个 DataFrame
        if sheet_name is None and isinstance(result, dict):
            if len(result) == 1:
                return list(result.values())[0]
            else:
                # 多个工作表时，返回第一个
                return list(result.values())[0]
        return result
    except FileNotFoundError:
        raise
    except ValueError as e:
        raise ValueError(f"工作表不存在或无效: {e}") from e
    except Exception as e:
        raise FileReadError(f"读取 Excel 文件失败: {e}") from e


def write_excel(
    data: pd.DataFrame | dict[str, pd.DataFrame],
    file_path: str,
    sheet_name: str = "Sheet1",
) -> None:
    """将数据写入 Excel 文件。

    支持写入单个 DataFrame 或多个 DataFrame（字典形式）。
    注意：此函数会覆盖整个目标文件，不保留原文件中的其他 Sheet。

    Args:
        data: 要写入的数据，可以是单个 DataFrame 或字典（多工作表）
        file_path: 输出 Excel 文件路径
        sheet_name: 工作表名称（当 data 为 DataFrame 时使用）

    Raises:
        ValueError: 数据格式无效
        PermissionError: 文件权限不足
        FileWriteError: 写入文件时发生错误

    Example:
        >>> # 写入单个 DataFrame
        >>> df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        >>> write_excel(df, "output.xlsx", sheet_name="Results")
        >>> # 写入多个工作表
        >>> data_dict = {"Sheet1": df1, "Sheet2": df2}
        >>> write_excel(data_dict, "output.xlsx")
    """
    if not isinstance(data, (pd.DataFrame, dict)):
        raise ValueError(
            f"数据格式无效，期望 DataFrame 或 dict，实际类型: {type(data)}"
        )

    # 如果是字典，先验证所有值都是 DataFrame
    if isinstance(data, dict):
        for sheet, df in data.items():
            if not isinstance(df, pd.DataFrame):
                raise ValueError(f"字典值必须是 DataFrame，实际类型: {type(df)}")

    try:
        if isinstance(data, pd.DataFrame):
            # 单个 DataFrame，写入指定工作表
            with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                data.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            # 字典形式，写入多个工作表
            with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                for sheet, df in data.items():
                    df.to_excel(writer, sheet_name=sheet, index=False)
    except PermissionError:
        raise
    except Exception as e:
        raise FileWriteError(f"写入 Excel 文件失败: {e}") from e


def get_sheet_names(file_path: str) -> list[str]:
    """获取 Excel 文件中的所有工作表名称。

    Args:
        file_path: Excel 文件路径

    Returns:
        工作表名称列表

    Raises:
        FileNotFoundError: 文件不存在
        FileReadError: 读取文件时发生错误

    Example:
        >>> sheets = get_sheet_names("data.xlsx")
        >>> print(sheets)
        ['Sheet1', 'Sheet2']
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    try:
        # 使用 pandas.ExcelFile 获取工作表名称
        with pd.ExcelFile(file_path) as excel_file:
            sheet_names: list[str] = excel_file.sheet_names
            return sheet_names
    except FileNotFoundError:
        raise
    except Exception as e:
        raise FileReadError(f"获取工作表名称失败: {e}") from e
