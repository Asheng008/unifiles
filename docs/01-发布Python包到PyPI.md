# 技术文档（一）：如何将 Python 项目发布到 PyPI

本文介绍如何将已开发好的 Python 库打包并发布到 [PyPI](https://pypi.org/)（Python Package Index），使他人可通过 `pip install your-package` 安装。以 Windows + PowerShell 环境为主，命令可直接在本机执行。

---

## 1. 前置条件

### 1.1 PyPI 账号

- **正式 PyPI**：在 [https://pypi.org/account/register/](https://pypi.org/account/register/) 注册账号。
- **TestPyPI**（建议先用于试发布）：在 [https://test.pypi.org/account/register/](https://test.pypi.org/account/register/) 单独注册，并完成邮箱验证。

两个站点账号独立，不能混用。

### 1.2 API Token（推荐）

发布时使用 API Token 比密码更安全：

- **TestPyPI**：登录后进入 [Account settings → API tokens](https://test.pypi.org/manage/account/#api-tokens)，创建 Token，Scope 选 “Entire account” 或指定项目。
- **正式 PyPI**：登录 [pypi.org](https://pypi.org) 后，[Account settings → API tokens](https://pypi.org/manage/account/#api-tokens) 创建 Token。

创建后**立即复制并保存** Token（含 `pypi-` 前缀），页面上只显示一次。

### 1.3 本地环境

- Python 3.9+（与项目 `requires-python` 一致）。
- 已创建并激活项目虚拟环境（推荐）。
- 升级 pip（可选但推荐）：
  ```powershell
  chcp 65001
  .\.venv\Scripts\Activate.ps1
  python -m pip install --upgrade pip
  ```

---

## 2. 项目结构要求

发布前需保证项目具备标准包结构及元数据，便于 `build` 和 `twine` 使用。

### 2.1 推荐目录结构（src 布局）

本仓库采用 **src 布局**，包代码放在 `src/` 下，与根目录配置文件分离：

```
项目根目录/
├── pyproject.toml    # 构建与元数据（必须）
├── README.md         # 项目说明，会展示在 PyPI 页面
├── LICENSE           # 许可证（强烈建议）
├── src/
│   └── your_package/ # 包名与 pyproject.toml 中 name 对应
│       ├── __init__.py
│       └── ...
└── tests/
```

`pyproject.toml` 中需声明包所在位置，例如使用 setuptools 时：

```toml
[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
```

### 2.2 pyproject.toml 必备内容

- **[build-system]**：指定构建后端（如 setuptools）。
- **[project]**：包名、版本、描述、Python 版本、依赖、分类等。

示例（节选）：

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "unifiles"           # PyPI 上的包名，只能含字母、数字、点、下划线、连字符
version = "0.1.0"
description = "统一的文件操作库，提供跨文件类型的统一接口"
readme = "README.md"
requires-python = ">=3.9"
license = {text = "MIT"}
authors = [{name = "your name", email = "your@email.com"}]
keywords = ["file", "excel", "pdf"]
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    # ...
]
dependencies = [
    "pandas>=2.0.0",
    # ...
]

[project.urls]
Homepage = "https://github.com/yourusername/unifiles"
Repository = "https://github.com/yourusername/unifiles"
Issues = "https://github.com/yourusername/unifiles/issues"
```

- **name**：在 PyPI 上必须唯一，若被占用需换名或使用 TestPyPI 测试。
- **version**：每次上传新版本必须递增，且不可覆盖或删除已发布版本。

### 2.3 README 与 LICENSE

- **README.md**：在 `readme = "README.md"` 中指定，会渲染到 PyPI 项目页。
- **LICENSE**：建议在项目根目录放置 LICENSE 文件，并在 `pyproject.toml` 中通过 `license` 和（若后端支持）`license-files` 声明，便于合规与自动包含进分发包。

---

## 3. 安装构建与上传工具

在项目虚拟环境中安装 `build` 和 `twine`：

```powershell
chcp 65001
.\.venv\Scripts\Activate.ps1
pip install --upgrade build twine
```

- **build**：根据 `pyproject.toml` 生成分发包（sdist + wheel）。
- **twine**：将生成的文件上传到 PyPI/TestPyPI，并校验元数据。

---

## 4. 构建分发包

在项目**根目录**（即 `pyproject.toml` 所在目录）执行：

```powershell
.\.venv\Scripts\Activate.ps1
python -m build
```

成功后会在根目录下生成 `dist/` 目录，通常包含：

- `your_package-0.1.0.tar.gz` — 源码分发包（sdist）
- `your_package-0.1.0-py3-none-any.whl` — 纯 Python 的 wheel（built distribution）

建议每次正式发布前清理旧构建再重新打包，避免误传旧文件：

```powershell
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
python -m build
```

---

## 5. 上传到 TestPyPI（建议先做）

先用 TestPyPI 验证打包与安装流程，再发正式 PyPI。

```powershell
.\.venv\Scripts\Activate.ps1
python -m twine upload --repository testpypi dist/*
```

按提示输入：

- **Username**：填 `__token__`
- **Password**：填 TestPyPI 的 API Token（含 `pypi-` 前缀）

上传成功后，可在 [https://test.pypi.org/project/your-package-name/](https://test.pypi.org/) 查看。安装测试：

```powershell
pip install --index-url https://test.pypi.org/simple/ --no-deps your-package-name
```

`--no-deps` 可避免从 TestPyPI 拉取依赖时出现版本或缺失问题；若需连同依赖一起测，可去掉该参数并在必要时指定 `--extra-index-url https://pypi.org/simple/`。

---

## 6. 上传到正式 PyPI

确认 TestPyPI 安装与使用正常后，再发正式 PyPI。

```powershell
.\.venv\Scripts\Activate.ps1
python -m twine upload dist/*
```

默认上传目标为正式 PyPI，无需加 `--repository`。同样：

- **Username**：`__token__`
- **Password**：正式 PyPI 的 API Token（含 `pypi-` 前缀）

成功后可在 [https://pypi.org/project/your-package-name/](https://pypi.org/) 查看，用户即可：

```powershell
pip install your-package-name
```

---

## 7. 使用 .pypirc 保存 Token（可选）

若不想每次输入用户名和 Token，可在用户目录下配置 `~/.pypirc`（Windows 下多为 `%USERPROFILE%\.pypirc`）。

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

注意：

- 不要将 `.pypirc` 提交到版本库；建议加入 `.gitignore`。
- 正式 PyPI 与 TestPyPI 的 Token 不同，需分别配置。

上传时指定仓库即可：

```powershell
# 仅上传到 TestPyPI
python -m twine upload --repository testpypi dist/*

# 上传到正式 PyPI（默认）
python -m twine upload dist/*
```

---

## 8. 发布流程小结（Windows / PowerShell）

| 步骤 | 命令 |
|------|------|
| 1. 激活环境 | `.\.venv\Scripts\Activate.ps1` |
| 2. 安装工具 | `pip install --upgrade build twine` |
| 3. 清理并构建 | `Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue; python -m build` |
| 4. 上传到 TestPyPI | `python -m twine upload --repository testpypi dist/*` |
| 5. 上传到正式 PyPI | `python -m twine upload dist/*` |

---

## 9. 常见问题与注意事项

- **包名已存在**：PyPI 包名全局唯一，若提示已占用，需在 `pyproject.toml` 中修改 `name`（或仅用 TestPyPI 测试）。
- **版本不可重复**：同一版本号只能上传一次，再次发布需在 `pyproject.toml` 中提高 `version` 并重新 `python -m build`。
- **Token 权限**：若 Token 仅限某项目，上传时需确保 `name` 与 Token 所关联项目一致。
- **网络与代理**：国内访问 PyPI 若较慢，可配置 pip/twine 使用镜像；上传一般仍需直连或配置好代理。
- **LICENSE 与 classifiers**：`license`、`classifiers` 与仓库中的 LICENSE 文件保持一致，避免法律与合规问题。

按上述步骤即可完成从本地项目到 PyPI 的发布；后续可结合 CI（如 GitHub Actions）实现“打 tag 或点按钮即构建并上传”，详见后续技术文档。
