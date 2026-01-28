# SQLite 模块开发计划（M5）

## 目标
实现 SQLite 数据库的查询和元数据获取功能，提供统一的 API 接口。

## 实现内容

### 1. 创建 `src/unifiles/sqlite.py` 模块

实现三个核心函数：

#### `query(db_path: str, sql: str, params: tuple | dict | None = None) -> pd.DataFrame`
- **功能**: 执行 SQL 查询并返回 DataFrame
- **实现方式**:
  - 使用 `import sqlite3` 和 `import pandas as pd`
  - 使用 `pathlib.Path` 检查数据库文件是否存在
  - 使用 `sqlite3.connect(db_path)` 创建连接
  - 使用 `pandas.read_sql_query(sql, conn, params=params)` 执行查询
  - 支持参数化查询：`params` 可以是 `tuple`（用于 `?` 占位符）或 `dict`（用于 `:name` 占位符）
  - 确保连接正确关闭（使用 `with` 语句）
- **错误处理**:
  - `FileNotFoundError`: 数据库文件不存在时抛出
  - `sqlite3.Error`: SQL 执行错误时抛出（保留原异常）
  - `FileReadError`: 其他读取错误时抛出
- **类型注解**: Python 3.9+ 风格（`tuple | dict | None`）
- **文档**: Google 风格 docstring，包含 Args、Returns、Raises、Example

#### `get_schema(db_path: str, table_name: str) -> dict[str, str]`
- **功能**: 获取表结构（字段名到字段类型的映射）
- **实现方式**:
  - 使用 `PRAGMA table_info(table_name)` 查询表结构
  - 从结果中提取 `name` 和 `type` 列
  - 构建 `dict[str, str]` 返回（字段名 -> 字段类型）
  - 验证表是否存在（如果 PRAGMA 返回空结果，说明表不存在）
- **错误处理**:
  - `FileNotFoundError`: 数据库文件不存在时抛出
  - `ValueError`: 表不存在时抛出
  - `FileReadError`: 读取错误时抛出
- **类型注解**: Python 3.9+ 风格
- **文档**: Google 风格 docstring

#### `get_tables(db_path: str) -> list[str]`
- **功能**: 获取数据库中所有表名列表
- **实现方式**:
  - 查询 `sqlite_master` 表：`SELECT name FROM sqlite_master WHERE type='table'`
  - 提取 `name` 列作为表名列表
  - 排除系统表（如 `sqlite_sequence`），只返回用户表
- **错误处理**:
  - `FileNotFoundError`: 数据库文件不存在时抛出
  - `FileReadError`: 读取错误时抛出
- **类型注解**: Python 3.9+ 风格
- **文档**: Google 风格 docstring

### 2. 编写测试文件 `tests/test_sqlite.py`

参考 `tests/test_excel.py` 和 `tests/test_word.py` 的测试模式，实现以下测试用例：

- `test_query_success(tmp_path)`: 测试正常查询
  - 创建测试数据库和表，插入测试数据
  - 执行 SELECT 查询，验证返回的 DataFrame 正确
- `test_query_with_params_tuple(tmp_path)`: 测试使用 tuple 参数化查询
  - 使用 `?` 占位符和 tuple 参数
- `test_query_with_params_dict(tmp_path)`: 测试使用 dict 参数化查询
  - 使用 `:name` 占位符和 dict 参数
- `test_query_file_not_found()`: 测试数据库不存在的情况
  - 验证抛出 `FileNotFoundError`
- `test_query_sql_error(tmp_path)`: 测试 SQL 错误
  - 执行无效 SQL，验证抛出 `sqlite3.Error`
- `test_get_schema_success(tmp_path)`: 测试获取表结构
  - 创建表，验证返回的 schema 字典正确
- `test_get_schema_table_not_found(tmp_path)`: 测试表不存在的情况
  - 验证抛出 `ValueError`
- `test_get_tables_success(tmp_path)`: 测试获取表名列表
  - 创建多个表，验证返回的表名列表正确
- `test_get_tables_empty(tmp_path)`: 测试空数据库
  - 验证返回空列表
- `test_get_tables_file_not_found()`: 测试数据库不存在的情况
  - 验证抛出 `FileNotFoundError`

### 3. 准备测试用的 SQLite 数据库

在测试中使用 `tmp_path` 动态创建测试数据库，包含：
- 示例表（如 `users`、`products`）
- 测试数据
- 不同的字段类型（INTEGER、TEXT、REAL 等）

### 4. 更新 `src/unifiles/__init__.py`

- 取消注释 SQLite 模块导入：`from .sqlite import query, get_schema, get_tables`
- 在 `__all__` 列表中添加 `query`、`get_schema`、`get_tables`

## 代码风格要求

参考 `src/unifiles/excel.py` 和 `src/unifiles/word.py` 的实现模式：
- 使用 `pathlib.Path` 进行路径操作
- 文件存在性检查：`path.exists()`
- 异常处理：先检查文件存在性，再捕获具体异常
- 使用自定义异常类：`FileReadError`
- 类型注解使用 Python 3.9+ 现代语法
- 数据库连接管理：使用 `with` 语句确保连接关闭

## 开发步骤

1. **查阅文档**: 确认 sqlite3 和 pandas.read_sql_query 的标准用法（已完成）
2. **实现 sqlite.py**: 编写三个函数，确保类型注解和错误处理完整
3. **编写测试**: 创建 `test_sqlite.py`，覆盖正常和异常流程
4. **更新导出**: 修改 `__init__.py` 导出新函数
5. **运行测试**: 确保所有测试通过
6. **代码质量检查**: 运行 mypy、black 检查

## 验收标准

- [ ] `sqlite.py` 模块实现完成，包含三个函数
- [ ] 所有函数有完整的类型注解（Python 3.9+ 风格）
- [ ] 所有函数有完整的 Google 风格 docstring
- [ ] 测试覆盖率 >= 80%
- [ ] 所有测试通过
- [ ] mypy 类型检查通过
- [ ] black 代码格式化通过
- [ ] `__init__.py` 正确导出新函数

## 技术要点

- **导入**: `import sqlite3`（标准库）、`import pandas as pd`
- **连接管理**: 使用 `with sqlite3.connect(db_path)` 确保连接关闭
- **参数化查询**: 
  - tuple: `params=(value1, value2)` 配合 `?` 占位符
  - dict: `params={'name': value}` 配合 `:name` 占位符
- **表结构查询**: 使用 `PRAGMA table_info(table_name)` 获取字段信息
- **表名查询**: 使用 `SELECT name FROM sqlite_master WHERE type='table'` 获取所有表名
- **pandas 集成**: 使用 `pd.read_sql_query()` 执行查询并返回 DataFrame

## 参考文件

- 实现参考: `src/unifiles/excel.py`、`src/unifiles/word.py`
- 测试参考: `tests/test_excel.py`、`tests/test_word.py`
- 异常定义: `src/unifiles/exceptions.py`
- 导出示例: `src/unifiles/__init__.py`

## 注意事项

- SQLite 数据库文件如果不存在，`sqlite3.connect()` 会创建新文件，但我们的函数应该要求文件已存在
- 参数化查询的类型：`params` 可以是 `tuple` 或 `dict`，需要正确处理两种类型
- 表名验证：`get_schema` 需要验证表是否存在（PRAGMA 返回空结果时）
- 系统表过滤：`get_tables` 应该只返回用户表，排除 `sqlite_sequence` 等系统表

## 实现细节

### query 函数实现要点

```python
def query(db_path: str, sql: str, params: tuple | dict | None = None) -> pd.DataFrame:
    path = Path(db_path)
    if not path.exists():
        raise FileNotFoundError(f"数据库文件不存在: {db_path}")
    
    try:
        with sqlite3.connect(db_path) as conn:
            # pandas.read_sql_query 会自动处理参数化查询
            df = pd.read_sql_query(sql, conn, params=params)
            return df
    except sqlite3.Error as e:
        raise  # 保留原异常
    except Exception as e:
        raise FileReadError(f"执行 SQL 查询失败: {e}") from e
```

### get_schema 函数实现要点

```python
def get_schema(db_path: str, table_name: str) -> dict[str, str]:
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
            schema = {row[1]: row[2] for row in rows}  # name -> type
            return schema
    except ValueError:
        raise
    except sqlite3.Error as e:
        raise FileReadError(f"获取表结构失败: {e}") from e
    except Exception as e:
        raise FileReadError(f"获取表结构失败: {e}") from e
```

### get_tables 函数实现要点

```python
def get_tables(db_path: str) -> list[str]:
    path = Path(db_path)
    if not path.exists():
        raise FileNotFoundError(f"数据库文件不存在: {db_path}")
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            # 过滤系统表（可选，根据需求决定）
            user_tables = [t for t in tables if not t.startswith('sqlite_')]
            return user_tables
    except sqlite3.Error as e:
        raise FileReadError(f"获取表名列表失败: {e}") from e
    except Exception as e:
        raise FileReadError(f"获取表名列表失败: {e}") from e
```

### 测试用例实现示例

```python
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

def test_query_with_params_tuple(tmp_path: Path):
    """测试 tuple 参数化查询。"""
    # ... 创建数据库和表 ...
    result = query(str(db_path), "SELECT * FROM users WHERE age > ?", (25,))
    assert len(result) == 1  # 只有 Bob 的年龄 > 25

def test_query_with_params_dict(tmp_path: Path):
    """测试 dict 参数化查询。"""
    # ... 创建数据库和表 ...
    result = query(str(db_path), "SELECT * FROM users WHERE age > :age", {"age": 25})
    assert len(result) == 1
```

## 任务清单

- [ ] 实现 `src/unifiles/sqlite.py` 模块
  - [ ] `query` 函数：执行 SQL 查询
  - [ ] `get_schema` 函数：获取表结构
  - [ ] `get_tables` 函数：获取所有表名
- [ ] 编写 `tests/test_sqlite.py` 测试文件
  - [ ] 正常流程测试（3个函数）
  - [ ] 参数化查询测试（tuple 和 dict）
  - [ ] 异常流程测试（文件不存在、SQL错误、表不存在）
- [ ] 更新 `src/unifiles/__init__.py` 导出函数
- [ ] 运行测试并验证代码质量
