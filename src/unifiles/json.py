"""JSON 文件操作模块。

提供 JSON 文件的读取、写入及与 YAML 的互转功能。
"""

import json
from pathlib import Path
from typing import Any

from .exceptions import FileReadError, FileWriteError


def read_json(file_path: str, encoding: str = "utf-8") -> Any:
    """读取 JSON 文件内容。

    Args:
        file_path: JSON 文件路径
        encoding: 文件编码，默认 utf-8

    Returns:
        解析后的 JSON 数据（通常为 dict 或 list）

    Raises:
        FileNotFoundError: 文件不存在
        FileReadError: 读取或解析 JSON 失败
        ValueError: JSON 格式错误

    Example:
        >>> data = read_json("config.json")
        >>> print(data['key'])
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    try:
        with path.open("r", encoding=encoding) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 格式错误: {e}") from e
    except Exception as e:
        raise FileReadError(f"读取 JSON 文件失败: {e}") from e


def write_json(
    data: Any,
    file_path: str,
    encoding: str = "utf-8",
    indent: int = 4,
    ensure_ascii: bool = False,
) -> None:
    """将数据写入 JSON 文件。

    Args:
        data: 要写入的数据（需可被 JSON 序列化）
        file_path: 输出文件路径
        encoding: 文件编码，默认 utf-8
        indent: 缩进空格数，默认 4
        ensure_ascii: 是否转义非 ASCII 字符，默认 False（支持中文直接显示）

    Raises:
        PermissionError: 权限不足
        TypeError: 数据无法序列化为 JSON
        FileWriteError: 写入失败

    Example:
        >>> write_json({"a": 1}, "data.json")
    """
    path = Path(file_path)
    try:
        with path.open("w", encoding=encoding) as f:
            json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
    except PermissionError:
        raise
    except TypeError as e:
        raise TypeError(f"数据无法序列化为 JSON: {e}") from e
    except Exception as e:
        raise FileWriteError(f"写入 JSON 文件失败: {e}") from e


def json_to_yaml(json_path: str, yaml_path: str, encoding: str = "utf-8") -> None:
    """将 JSON 文件转换为 YAML 文件。

    Args:
        json_path: 源 JSON 文件路径
        yaml_path: 目标 YAML 文件路径
        encoding: 文件编码，默认 utf-8

    Raises:
        FileNotFoundError: 源文件不存在
        FileReadError: 读取源文件失败
        FileWriteError: 写入目标文件失败
    """
    # 延迟导入以避免循环依赖
    from .yaml import write_yaml

    data = read_json(json_path, encoding=encoding)
    write_yaml(data, yaml_path, encoding=encoding)
