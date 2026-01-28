"""Excel 模块测试用例。"""

import pytest
import pandas as pd
from pathlib import Path

from unifiles.excel import read_excel, write_excel, get_sheet_names
from unifiles.exceptions import FileReadError, FileWriteError


def test_read_excel_success(tmp_path: Path):
    """测试成功读取 Excel 文件。"""
    # 创建测试文件
    test_file = tmp_path / "test.xlsx"
    df_expected = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    # 使用 ExcelWriter 确保文件格式正确
    with pd.ExcelWriter(test_file, engine="openpyxl") as writer:
        df_expected.to_excel(writer, sheet_name="Sheet1", index=False)

    # 测试读取
    result = read_excel(str(test_file))
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3
    assert list(result.columns) == ["A", "B"]
    pd.testing.assert_frame_equal(result, df_expected)


def test_read_excel_sheet_name(tmp_path: Path):
    """测试指定工作表名称读取。"""
    test_file = tmp_path / "test.xlsx"
    df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    df2 = pd.DataFrame({"C": [5, 6], "D": [7, 8]})

    with pd.ExcelWriter(test_file, engine="openpyxl") as writer:
        df1.to_excel(writer, sheet_name="Sheet1", index=False)
        df2.to_excel(writer, sheet_name="Sheet2", index=False)

    # 读取指定工作表
    result = read_excel(str(test_file), sheet_name="Sheet2")
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["C", "D"]
    pd.testing.assert_frame_equal(result, df2)


def test_read_excel_sheet_index(tmp_path: Path):
    """测试使用索引读取工作表。"""
    test_file = tmp_path / "test.xlsx"
    df1 = pd.DataFrame({"A": [1, 2]})
    df2 = pd.DataFrame({"B": [3, 4]})

    with pd.ExcelWriter(test_file, engine="openpyxl") as writer:
        df1.to_excel(writer, sheet_name="Sheet1", index=False)
        df2.to_excel(writer, sheet_name="Sheet2", index=False)

    # 使用索引读取第二个工作表
    result = read_excel(str(test_file), sheet_name=1)
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["B"]


def test_read_excel_file_not_found():
    """测试文件不存在的情况。"""
    with pytest.raises(FileNotFoundError, match="文件不存在"):
        read_excel("nonexistent.xlsx")


def test_read_excel_invalid_sheet(tmp_path: Path):
    """测试无效工作表的情况。"""
    test_file = tmp_path / "test.xlsx"
    df = pd.DataFrame({"A": [1, 2, 3]})
    df.to_excel(test_file, index=False)

    # 测试不存在的工作表名称
    with pytest.raises(ValueError, match="工作表不存在或无效"):
        read_excel(str(test_file), sheet_name="NonExistentSheet")

    # 测试超出范围的索引
    with pytest.raises(ValueError):
        read_excel(str(test_file), sheet_name=999)


def test_write_excel_dataframe(tmp_path: Path):
    """测试写入单个 DataFrame。"""
    test_file = tmp_path / "output.xlsx"
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

    write_excel(df, str(test_file), sheet_name="Results")

    # 验证文件已创建
    assert test_file.exists()

    # 验证内容
    result = read_excel(str(test_file), sheet_name="Results")
    pd.testing.assert_frame_equal(result, df)


def test_write_excel_dict(tmp_path: Path):
    """测试写入多工作表。"""
    test_file = tmp_path / "output.xlsx"
    df1 = pd.DataFrame({"A": [1, 2]})
    df2 = pd.DataFrame({"B": [3, 4]})
    data_dict = {"Sheet1": df1, "Sheet2": df2}

    write_excel(data_dict, str(test_file))

    # 验证文件已创建
    assert test_file.exists()

    # 验证两个工作表都存在
    sheets = get_sheet_names(str(test_file))
    assert "Sheet1" in sheets
    assert "Sheet2" in sheets

    # 验证内容
    result1 = read_excel(str(test_file), sheet_name="Sheet1")
    result2 = read_excel(str(test_file), sheet_name="Sheet2")
    pd.testing.assert_frame_equal(result1, df1)
    pd.testing.assert_frame_equal(result2, df2)


def test_write_excel_overwrite(tmp_path: Path):
    """测试覆盖文件，验证不保留原有其他 Sheet。"""
    test_file = tmp_path / "output.xlsx"

    # 第一次写入，包含两个工作表
    df1 = pd.DataFrame({"A": [1, 2]})
    df2 = pd.DataFrame({"B": [3, 4]})
    write_excel({"Sheet1": df1, "Sheet2": df2}, str(test_file))

    # 验证两个工作表都存在
    sheets_before = get_sheet_names(str(test_file))
    assert len(sheets_before) == 2
    assert "Sheet1" in sheets_before
    assert "Sheet2" in sheets_before

    # 第二次写入，只写入一个工作表
    df3 = pd.DataFrame({"C": [5, 6]})
    write_excel(df3, str(test_file), sheet_name="Sheet3")

    # 验证现在只有一个工作表
    sheets_after = get_sheet_names(str(test_file))
    assert len(sheets_after) == 1
    assert "Sheet3" in sheets_after
    assert "Sheet1" not in sheets_after
    assert "Sheet2" not in sheets_after


def test_write_excel_invalid_data(tmp_path: Path):
    """测试无效数据格式。"""
    test_file = tmp_path / "output.xlsx"

    # 测试非 DataFrame 和非 dict 类型
    with pytest.raises(ValueError, match="数据格式无效"):
        write_excel("invalid_data", str(test_file))

    # 测试 dict 中值不是 DataFrame
    with pytest.raises(ValueError, match="字典值必须是 DataFrame"):
        write_excel({"Sheet1": "invalid"}, str(test_file))


def test_get_sheet_names(tmp_path: Path):
    """测试获取工作表名称。"""
    test_file = tmp_path / "test.xlsx"
    df1 = pd.DataFrame({"A": [1]})
    df2 = pd.DataFrame({"B": [2]})
    df3 = pd.DataFrame({"C": [3]})

    with pd.ExcelWriter(test_file, engine="openpyxl") as writer:
        df1.to_excel(writer, sheet_name="Sheet1", index=False)
        df2.to_excel(writer, sheet_name="Sheet2", index=False)
        df3.to_excel(writer, sheet_name="Sheet3", index=False)

    sheets = get_sheet_names(str(test_file))
    assert isinstance(sheets, list)
    assert len(sheets) == 3
    assert "Sheet1" in sheets
    assert "Sheet2" in sheets
    assert "Sheet3" in sheets


def test_get_sheet_names_file_not_found():
    """测试文件不存在的情况。"""
    with pytest.raises(FileNotFoundError, match="文件不存在"):
        get_sheet_names("nonexistent.xlsx")
