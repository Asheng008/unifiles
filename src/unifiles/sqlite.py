"""SQLite 数据库操作模块。

提供 SQLite 数据库的查询和元数据获取功能。
"""

import sqlite3
from pathlib import Path

import pandas as pd
from pandas.errors import DatabaseError

from .exceptions import FileReadError


def query(db_path: str, sql: str, params: tuple | dict | None = None) -> pd.DataFrame:
    """执行 SQL 查询并返回 DataFrame。

    Args:
        db_path: SQLite 数据库文件路径
        sql: SQL 查询语句
        params: 查询参数，可以是 tuple（用于 ? 占位符）或 dict（用于 :name 占位符）

    Returns:
        包含查询结果的 DataFrame 对象

    Raises:
        FileNotFoundError: 数据库文件不存在
        sqlite3.Error: SQL 执行错误
        FileReadError: 读取数据库时发生错误

    Example:
        >>> # 简单查询
        >>> df = query("database.db", "SELECT * FROM users")
        >>> # 使用 tuple 参数化查询
        >>> df = query("database.db", "SELECT * FROM users WHERE age > ?", (18,))
        >>> # 使用 dict 参数化查询
        >>> df = query("database.db", "SELECT * FROM users WHERE age > :age", {"age": 18})
    """
    path = Path(db_path)
    if not path.exists():
        raise FileNotFoundError(f"数据库文件不存在: {db_path}")

    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query(sql, conn, params=params)
            return df
    except DatabaseError as e:
        # pandas 会将 sqlite3.Error 包装为 DatabaseError
        # 检查底层原因是否是 sqlite3.Error
        if isinstance(e.__cause__, sqlite3.Error):
            raise e.__cause__  # 抛出原始的 sqlite3.Error
        raise sqlite3.Error(str(e)) from e
    except sqlite3.Error:
        raise  # 保留原异常
    except Exception as e:
        raise FileReadError(f"执行 SQL 查询失败: {e}") from e


def get_schema(db_path: str, table_name: str) -> dict[str, str]:
    """获取表结构（字段名到字段类型的映射）。

    Args:
        db_path: SQLite 数据库文件路径
        table_name: 表名

    Returns:
        字段名到字段类型的字典映射

    Raises:
        FileNotFoundError: 数据库文件不存在
        ValueError: 表不存在
        FileReadError: 读取数据库时发生错误

    Example:
        >>> schema = get_schema("database.db", "users")
        >>> print(schema)
        {'id': 'INTEGER', 'name': 'TEXT', 'age': 'INTEGER'}
    """
    path = Path(db_path)
    if not path.exists():
        raise FileNotFoundError(f"数据库文件不存在: {db_path}")

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            rows = cursor.fetchall()

            if not rows:
                raise ValueError(f"表不存在: {table_name}")

            # PRAGMA table_info 返回: (cid, name, type, notnull, dflt_value, pk)
            # 提取 name (索引1) 和 type (索引2)
            schema: dict[str, str] = {row[1]: row[2] for row in rows}
            return schema
    except ValueError:
        raise
    except sqlite3.Error as e:
        raise FileReadError(f"获取表结构失败: {e}") from e
    except Exception as e:
        raise FileReadError(f"获取表结构失败: {e}") from e


def get_tables(db_path: str) -> list[str]:
    """获取数据库中所有表名列表。

    Args:
        db_path: SQLite 数据库文件路径

    Returns:
        表名列表（排除系统表）

    Raises:
        FileNotFoundError: 数据库文件不存在
        FileReadError: 读取数据库时发生错误

    Example:
        >>> tables = get_tables("database.db")
        >>> print(tables)
        ['users', 'products', 'orders']
    """
    path = Path(db_path)
    if not path.exists():
        raise FileNotFoundError(f"数据库文件不存在: {db_path}")

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            # 过滤系统表（以 sqlite_ 开头的表）
            user_tables: list[str] = [t for t in tables if not t.startswith("sqlite_")]
            return user_tables
    except sqlite3.Error as e:
        raise FileReadError(f"获取表名列表失败: {e}") from e
    except Exception as e:
        raise FileReadError(f"获取表名列表失败: {e}") from e
