"""表格处理辅助函数。"""

from docx.table import Table


def table_to_list(table: Table) -> list[list[str]]:
    """将 python-docx 表格转换为二维列表。

    Args:
        table: python-docx 表格对象

    Returns:
        二维字符串列表，空表格返回空列表
    """
    if not table.rows:
        return []

    rows_data: list[list[str]] = []
    for row in table.rows:
        row_data = [cell.text.strip() for cell in row.cells]
        rows_data.append(row_data)

    return rows_data


def list_to_markdown(data: list[list[str]]) -> str:
    """将二维列表转换为 Markdown 表格字符串。

    Args:
        data: 二维字符串列表

    Returns:
        Markdown 格式的表格字符串，空列表返回空字符串
    """
    if not data:
        return ""

    col_count = max(len(row) for row in data)
    lines = []

    header = data[0] + [""] * (col_count - len(data[0]))
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * col_count) + " |")

    for row in data[1:]:
        formatted_row = list(row) + [""] * (col_count - len(row))
        formatted_row = [cell if cell else " " for cell in formatted_row]
        lines.append("| " + " | ".join(formatted_row) + " |")

    return "\n".join(lines)
