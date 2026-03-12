"""YAML 文件操作模块。

提供 YAML 文件的读取、写入及与 JSON 的互转功能。
"""

from pathlib import Path
from typing import Any

import yaml

from .exceptions import FileReadError, FileWriteError


def read_yaml(file_path: str, encoding: str = "utf-8") -> Any:
    """读取 YAML 文件内容。

    Args:
        file_path: YAML 文件路径
        encoding: 文件编码，默认 utf-8

    Returns:
        解析后的 YAML 数据（通常为 dict 或 list）

    Raises:
        FileNotFoundError: 文件不存在
        FileReadError: 读取或解析 YAML 失败
        ValueError: YAML 格式错误

    Example:
        >>> data = read_yaml("config.yaml")
        >>> print(data['key'])
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    try:
        with path.open("r", encoding=encoding) as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"YAML 格式错误: {e}") from e
    except Exception as e:
        raise FileReadError(f"读取 YAML 文件失败: {e}") from e


def write_yaml(
    data: Any,
    file_path: str,
    encoding: str = "utf-8",
    allow_unicode: bool = True,
    sort_keys: bool = False,
) -> None:
    """将数据写入 YAML 文件。

    Args:
        data: 要写入的数据（需可被 YAML 序列化）
        file_path: 输出文件路径
        encoding: 文件编码，默认 utf-8
        allow_unicode: 是否允许 Unicode 字符（支持中文直接显示），默认 True
        sort_keys: 是否对键进行排序，默认 False

    Raises:
        PermissionError: 权限不足
        FileWriteError: 写入失败

    Example:
        >>> write_yaml({"a": 1}, "data.yaml")
    """
    path = Path(file_path)
    try:
        with path.open("w", encoding=encoding) as f:
            yaml.safe_dump(data, f, allow_unicode=allow_unicode, sort_keys=sort_keys)
    except PermissionError:
        raise
    except Exception as e:
        raise FileWriteError(f"写入 YAML 文件失败: {e}") from e


def yaml_to_json(
    yaml_path: str,
    json_path: str,
    encoding: str = "utf-8",
    indent: int = 4,
    ensure_ascii: bool = False,
) -> None:
    """将 YAML 文件转换为 JSON 文件。

    Args:
        yaml_path: 源 YAML 文件路径
        json_path: 目标 JSON 文件路径
        encoding: 文件编码，默认 utf-8
        indent: JSON 缩进空格数，默认 4
        ensure_ascii: JSON 是否转义非 ASCII 字符，默认 False

    Raises:
        FileNotFoundError: 源文件不存在
        FileReadError: 读取源文件失败
        FileWriteError: 写入目标文件失败
    """
    # 延迟导入以避免循环依赖
    from .json import write_json

    data = read_yaml(yaml_path, encoding=encoding)
    write_json(
        data, json_path, encoding=encoding, indent=indent, ensure_ascii=ensure_ascii
    )
