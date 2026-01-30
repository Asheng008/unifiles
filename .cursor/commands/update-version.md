# 更新版本号及 CHANGELOG

根据语义化版本规范（SemVer）更新项目版本号，并同步更新 CHANGELOG.md 记录。

## 使用方式

- 在 Cursor 命令面板或聊天中触发：
  - `/update-version`

> **注意**：此命令会修改版本号文件和 CHANGELOG.md，请确保已保存所有更改。

## 版本号规则

根据语义化版本规范（`MAJOR.MINOR.PATCH`）：

- **MAJOR（大版本）**：破坏性变更（不兼容改动）
  - 例如：`0.3.0` → `1.0.0`
- **MINOR（小版本）**：向后兼容的新功能
  - 例如：`0.3.0` → `0.4.0`
- **PATCH（补丁版本）**：Bug 修复/小改进
  - 例如：`0.3.0` → `0.3.1`

## 必做步骤

### 1. 读取当前版本号

从 `src/unifiles/__init__.py` 或 `pyproject.toml` 中读取当前版本号。

### 2. 确定新版本号

**方式一：自动计算（推荐）**
- 询问用户要升级的类型（MAJOR/MINOR/PATCH）
- 根据当前版本号自动计算新版本号

**方式二：手动指定**
- 让用户直接输入新版本号（格式：`X.Y.Z`）

### 3. 更新版本号文件

需要更新以下两个文件：

**文件 1：`src/unifiles/__init__.py`**
```python
__version__ = "X.Y.Z"  # 更新为新版本号
```

**文件 2：`pyproject.toml`**
```toml
[project]
version = "X.Y.Z"  # 更新为新版本号
```

### 4. 更新 CHANGELOG.md

将 `[Unreleased]` 部分的内容移动到新版本小节，格式如下：

```markdown
## [Unreleased]

- （在开发下一个版本时，将改动先记录在这里；发布时再移动到对应版本小节）

## [X.Y.Z] - YYYY-MM-DD

### Added
- （从 Unreleased 移动过来的内容）

### Changed
- （从 Unreleased 移动过来的内容）

### Fixed
- （从 Unreleased 移动过来的内容）

### Removed
- （从 Unreleased 移动过来的内容）

### Deprecated
- （从 Unreleased 移动过来的内容）

## [旧版本号] - YYYY-MM-DD
...
```

**注意事项**：
- 日期格式：`YYYY-MM-DD`（例如：`2026-01-30`）
- 如果 `[Unreleased]` 为空，仍需要创建新版本小节（可以只包含版本号和日期）
- 保持 CHANGELOG 的格式和结构一致

### 5. 验证更新

更新完成后，验证以下内容：
- `src/unifiles/__init__.py` 中的版本号已更新
- `pyproject.toml` 中的版本号已更新
- `CHANGELOG.md` 中已添加新版本小节
- 两个位置的版本号一致

## 执行流程示例

### 场景 1：自动计算 MINOR 版本（推荐）

**当前版本**：`0.3.0`

**用户选择**：MINOR（新增功能）

**新版本**：`0.4.0`

**操作**：
1. 更新 `__init__.py`：`__version__ = "0.4.0"`
2. 更新 `pyproject.toml`：`version = "0.4.0"`
3. 更新 `CHANGELOG.md`：将 `[Unreleased]` 内容移动到 `[0.4.0] - 2026-01-30`

### 场景 2：手动指定版本号

**当前版本**：`0.3.0`

**用户输入**：`1.0.0`

**操作**：
1. 更新 `__init__.py`：`__version__ = "1.0.0"`
2. 更新 `pyproject.toml`：`version = "1.0.0"`
3. 更新 `CHANGELOG.md`：将 `[Unreleased]` 内容移动到 `[1.0.0] - 2026-01-30`

## 实现提示

1. **读取当前版本**：
   - 优先从 `src/unifiles/__init__.py` 读取 `__version__`
   - 或从 `pyproject.toml` 的 `[project]` 部分读取 `version`

2. **版本号解析**：
   - 使用正则表达式或字符串分割解析 `MAJOR.MINOR.PATCH`
   - 验证版本号格式有效性

3. **日期获取**：
   - 使用当前日期（格式：`YYYY-MM-DD`）
   - 在 Windows PowerShell 中可以使用：`Get-Date -Format "yyyy-MM-dd"`

4. **CHANGELOG 更新**：
   - 读取 `CHANGELOG.md` 文件
   - 找到 `[Unreleased]` 部分
   - 提取其内容（如果有）
   - 在 `[Unreleased]` 后插入新版本小节
   - 清空或重置 `[Unreleased]` 部分

5. **错误处理**：
   - 如果版本号格式无效，提示用户
   - 如果 `CHANGELOG.md` 格式异常，提示用户手动检查
   - 确保两个版本号文件同步更新

## 后续步骤

版本号更新完成后，建议：

1. **运行测试**：确保版本号更新不影响功能
   ```powershell
   pytest
   ```

2. **提交更改**：
   ```powershell
   git add src/unifiles/__init__.py pyproject.toml CHANGELOG.md
   git commit -m "chore: 更新版本号至 X.Y.Z"
   ```

3. **创建 Git Tag**（准备发布时）：
   ```powershell
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

4. **发布到 PyPI**（如果配置了自动发布）：
   - 推送 Tag 后，GitHub Actions 会自动触发发布流程

## 注意事项

- ⚠️ **版本号一致性**：确保 `__init__.py` 和 `pyproject.toml` 中的版本号完全一致
- ⚠️ **CHANGELOG 格式**：保持与现有格式一致，使用标准的 Markdown 格式
- ⚠️ **日期格式**：使用 `YYYY-MM-DD` 格式（ISO 8601）
- ⚠️ **语义化版本**：遵循 SemVer 规范，确保版本号升级符合变更类型
