"""SQLite 模块测试用例。"""

import pytest
import sqlite3
import pandas as pd
from pathlib import Path

from unifiles.sqlite import query, get_schema, get_tables
from unifiles.exceptions import FileReadError


def test_query_success(tmp_path: Path):
    """测试正常查询。"""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT, age INTEGER)")
    cursor.execute("INSERT INTO users VALUES (1, 'Alice', 25)")
    cursor.execute("INSERT INTO users VALUES (2, 'Bob', 30)")
    conn.commit()
    conn.close()

    result = query(str(db_path), "SELECT * FROM users")
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert list(result.columns) == ["id", "name", "age"]
    assert result.iloc[0]["name"] == "Alice"
    assert result.iloc[1]["name"] == "Bob"


def test_query_with_params_tuple(tmp_path: Path):
    """测试使用 tuple 参数化查询。"""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT, age INTEGER)")
    cursor.execute("INSERT INTO users VALUES (1, 'Alice', 25)")
    cursor.execute("INSERT INTO users VALUES (2, 'Bob', 30)")
    cursor.execute("INSERT INTO users VALUES (3, 'Charlie', 35)")
    conn.commit()
    conn.close()

    result = query(str(db_path), "SELECT * FROM users WHERE age > ?", (25,))
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2  # 只有 Bob 和 Charlie 的年龄 > 25
    assert "Bob" in result["name"].values
    assert "Charlie" in result["name"].values
    assert "Alice" not in result["name"].values


def test_query_with_params_dict(tmp_path: Path):
    """测试使用 dict 参数化查询。"""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT, age INTEGER)")
    cursor.execute("INSERT INTO users VALUES (1, 'Alice', 25)")
    cursor.execute("INSERT INTO users VALUES (2, 'Bob', 30)")
    conn.commit()
    conn.close()

    result = query(str(db_path), "SELECT * FROM users WHERE age > :age", {"age": 25})
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1  # 只有 Bob 的年龄 > 25
    assert result.iloc[0]["name"] == "Bob"


def test_query_without_params(tmp_path: Path):
    """测试不带参数的查询。"""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'Alice')")
    conn.commit()
    conn.close()

    result = query(str(db_path), "SELECT * FROM users")
    assert len(result) == 1
    assert result.iloc[0]["name"] == "Alice"


def test_query_file_not_found():
    """测试数据库不存在的情况。"""
    with pytest.raises(FileNotFoundError, match="数据库文件不存在"):
        query("nonexistent.db", "SELECT * FROM users")


def test_query_sql_error(tmp_path: Path):
    """测试 SQL 错误。"""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    conn.commit()
    conn.close()

    # 执行无效 SQL
    with pytest.raises(sqlite3.Error):
        query(str(db_path), "SELECT * FROM nonexistent_table")


def test_get_schema_success(tmp_path: Path):
    """测试获取表结构。"""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, score REAL)"
    )
    conn.commit()
    conn.close()

    schema = get_schema(str(db_path), "users")
    assert isinstance(schema, dict)
    assert "id" in schema
    assert "name" in schema
    assert "age" in schema
    assert "score" in schema
    assert schema["id"] == "INTEGER"
    assert schema["name"] == "TEXT"
    assert schema["age"] == "INTEGER"
    assert schema["score"] == "REAL"


def test_get_schema_table_not_found(tmp_path: Path):
    """测试表不存在的情况。"""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER)")
    conn.commit()
    conn.close()

    with pytest.raises(ValueError, match="表不存在"):
        get_schema(str(db_path), "nonexistent_table")


def test_get_schema_file_not_found():
    """测试数据库不存在的情况。"""
    with pytest.raises(FileNotFoundError, match="数据库文件不存在"):
        get_schema("nonexistent.db", "users")


def test_get_tables_success(tmp_path: Path):
    """测试获取表名列表。"""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER)")
    cursor.execute("CREATE TABLE products (id INTEGER)")
    cursor.execute("CREATE TABLE orders (id INTEGER)")
    conn.commit()
    conn.close()

    tables = get_tables(str(db_path))
    assert isinstance(tables, list)
    assert len(tables) == 3
    assert "users" in tables
    assert "products" in tables
    assert "orders" in tables


def test_get_tables_empty(tmp_path: Path):
    """测试空数据库。"""
    db_path = tmp_path / "test.db"
    # 创建空数据库
    conn = sqlite3.connect(db_path)
    conn.close()

    tables = get_tables(str(db_path))
    assert isinstance(tables, list)
    assert len(tables) == 0


def test_get_tables_excludes_system_tables(tmp_path: Path):
    """测试排除系统表。"""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT)")
    cursor.execute("INSERT INTO users DEFAULT VALUES")
    conn.commit()
    conn.close()

    # sqlite_sequence 是系统表，应该被排除
    tables = get_tables(str(db_path))
    assert "users" in tables
    assert "sqlite_sequence" not in tables


def test_get_tables_file_not_found():
    """测试数据库不存在的情况。"""
    with pytest.raises(FileNotFoundError, match="数据库文件不存在"):
        get_tables("nonexistent.db")
