# 技术文档（三）：用 GitHub Actions 自动发布到 TestPyPI / PyPI

本篇在前两篇基础上，专门介绍如何使用 **GitHub Actions + Trusted Publishing + 官方 Action** 实现：

- **推送 Tag 自动发布到正式 PyPI**
- **推送到 main 分支自动发布到 TestPyPI（可选）**

参考文档为 Python Packaging 官方指南：  
《Publishing package distribution releases using GitHub Actions CI/CD workflows》。

---

## 1. 整体思路与最佳实践

结合官方推荐，本项目的自动发布策略建议：

- **构建与发布分离**：
  - 一个 Job 负责构建分发包（sdist + wheel），并用 `upload-artifact` 暂存。
  - 另两个 Job 负责从 artifact 下载包并发布到 TestPyPI / PyPI。
- **仅在打 Tag 时发布到 PyPI 正式库**：
  - 通过 `if: startsWith(github.ref, 'refs/tags/')` 限制，只在打版本 Tag（如 `v0.1.0`）时发布。
- **使用 Trusted Publishing（OIDC）而不是手动 API Token（推荐做法）**：
  - 在 PyPI / TestPyPI 后台配置 **Trusted Publisher**，GitHub 通过 OpenID Connect 动态获取短期 token。
  - 不再需要在 GitHub Secrets 里存放长期 API Token（安全性更好）。
- **TestPyPI 与 PyPI 分开 Job / 环境**：
  - TestPyPI：更频繁、自动发布，用于验证发布流程。
  - PyPI：推荐要求手动审批（GitHub Environment 审批），降低误发风险。

---

## 2. 前置条件

### 2.1 项目准备

确保前两篇文档中的内容已经完成：

- `pyproject.toml` 配置正确（`name`、`version`、`license` 等）。
- 本地可以用 `python -m build` 成功构建分发包。
- CI（`ci.yml`）已经能在 push / PR 时顺利通过（black/mypy/pytest/build）。

### 2.2 PyPI / TestPyPI 账号与项目

- 拥有 **PyPI** 账号，并可以访问：
  - `https://pypi.org/manage/account/publishing/`
- 拥有 **TestPyPI** 账号（与 PyPI 独立）：
  - `https://test.pypi.org/manage/account/publishing/`
- 项目名（`unifiles`）在 PyPI / TestPyPI 中尚未被占用（第一次使用 Trusted Publishing 会自动创建项目）。

---

## 3. 在 PyPI / TestPyPI 配置 Trusted Publishing

下面过程基本照搬官方指南，只是结合 `unifiles` 做说明。

### 3.1 在 PyPI 创建 Trusted Publisher

1. 登录 PyPI，访问：`https://pypi.org/manage/account/publishing/`  
2. 填写：
   - **Project name**：`unifiles`（与你 `pyproject.toml` 的 `name` 一致）
   - **GitHub owner**：你的 GitHub 用户名或组织名（例如：`Asheng008`）
   - **GitHub repository**：仓库名（例如：`unifiles`）
   - **Workflow filename**：发布工作流文件名（例如：`.github/workflows/publish.yml`）
   - **Environment name**：`pypi`
3. 提交后，将看到一个 “pending” 的 Trusted Publisher，首次成功发布后会变为 active。

### 3.2 在 TestPyPI 创建 Trusted Publisher

重复上述步骤，只是：

1. 登录 TestPyPI：`https://test.pypi.org/manage/account/publishing/`
2. 配置时 **Environment name** 填写：`testpypi`

> 提示：如果之前按照旧版本教程创建过 `PYPI_API_TOKEN` / `TEST_PYPI_API_TOKEN`，官方现在建议 **改用 Trusted Publishing**，可以在 PyPI / TestPyPI 帐户设置里撤销旧 Token，并删除 GitHub 仓库中的对应 Secrets。

---

## 4. 创建发布工作流 `publish.yml`

在仓库中创建：

```text
.github/
└── workflows/
    └── publish.yml
```

### 4.1 完整示例：`publish.yml`

下面示例基于官方推荐做了简化，并适配 `unifiles`：

```yaml
name: Publish Python distribution to PyPI and TestPyPI

on:
  push:
    tags:
      - "v*"        # 只有打 tag（例如 v0.1.0）时才触发发布

jobs:
  build:
    name: Build distribution
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install build
        run: |
          python -m pip install --upgrade pip
          pip install build

      - name: Build sdist and wheel
        run: python -m build

      - name: Upload dist artifacts
        uses: actions/upload-artifact@v4
        with:
          name: python-package-distributions
          path: dist/

  publish-to-testpypi:
    name: Publish to TestPyPI
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: testpypi
      url: https://test.pypi.org/p/unifiles
    permissions:
      id-token: write    # Trusted Publishing 必须

    steps:
      - name: Download all dists
        uses: actions/download-artifact@v4
        with:
          name: python-package-distributions
          path: dist/

      - name: Publish distribution to TestPyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          repository-url: https://test.pypi.org/legacy/

  publish-to-pypi:
    name: Publish to PyPI
    needs: build
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')
    environment:
      name: pypi
      url: https://pypi.org/p/unifiles
    permissions:
      id-token: write    # Trusted Publishing 必须

    steps:
      - name: Download all dists
        uses: actions/download-artifact@v4
        with:
          name: python-package-distributions
          path: dist/

      - name: Publish distribution to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

### 4.2 关键点说明

- **on.push.tags: "v\*"**：
  - 只有推送形如 `v0.1.0` 的 Tag 才会触发发布，避免普通提交误发版本。
- **build Job**：
  - 只负责构建 `dist/`，并用 `upload-artifact` 存起来。
- **publish-to-testpypi / publish-to-pypi Job**：
  - 都依赖 `build`，先 `download-artifact`，再调用 `pypa/gh-action-pypi-publish`。
  - `permissions.id-token: write` 打开 OIDC 权限，为 Trusted Publishing 提供临时凭证。
  - `environment.name` 必须与 PyPI/TestPyPI 后台配置的环境名一致（`pypi` / `testpypi`）。
  - TestPyPI 通过 `repository-url: https://test.pypi.org/legacy/` 指向测试仓库。

> **安全建议**：  
> - 在 GitHub 仓库的 **Settings → Environments** 中，对 `pypi` 环境开启 “Required reviewers”（手动审批），让正式发布需要你点一次确认。  
> - `testpypi` 环境一般不必强制审批，可以每次 Tag 都自动发一份，保证流水线长期健康。

---

## 5. 与本地发布脚本的关系

你现在有三条发布路径：

1. **本地批处理脚本 `publish_pypi.bat`**：
   - 适合同步开发、调试版本、网络/环境受限时手动发布。
2. **手工命令（第一篇文档中的 PowerShell 命令）**：
   - 最原始、最透明的方式，用于理解底层原理。
3. **GitHub Actions 自动发布（本篇）**：
   - 适合稳定版本：打 Tag → CI 跑完 → 自动发布 TestPyPI / PyPI。

推荐用法：

- 开发阶段：本地跑批处理脚本 / 手动命令，快速验证。
- 准备正式版本：
  1. 更新 `pyproject.toml` 里的 `version`。
  2. 提交代码并 push 到 GitHub，确保 CI 通过。
  3. 打 Tag：`git tag v0.1.0 && git push origin v0.1.0`。
  4. 等 GitHub Actions 中 `publish` workflow 跑完，检查 TestPyPI / PyPI 页面。

---

## 6. 故障排查小贴士

### 6.1 Trusted Publishing 配置错误

常见现象：

- `pypa/gh-action-pypi-publish` 报权限错误，或找不到对应项目。

排查步骤：

- 检查 PyPI / TestPyPI 后台 Trusted Publisher：
  - project name 是否是 `unifiles`。
  - GitHub owner / repo 名是否和实际仓库一致。
  - workflow 文件名是否为 `.github/workflows/publish.yml`。
  - environment 名是否为 `pypi` / `testpypi`。
- 检查 GitHub `publish.yml` 中：
  - `environment.name` 是否与上面配置一致。
  - 是否设置了 `permissions: id-token: write`。

### 6.2 构建失败

- 查看 `build` Job 的日志，重点关注：
  - `python -m build` 前后的输出。
  - 是否有打包脚本、元数据（版本号、依赖等）的问题。

### 6.3 版本号重复

- PyPI / TestPyPI 不允许覆盖同一版本：
  - 调整 `pyproject.toml` 中的 `version`，比如从 `0.1.0` 升到 `0.1.1`，重新打 Tag 发布。

---

## 7. 小结

通过本篇配置好 `publish.yml` 和 Trusted Publishing 后：

- 你可以做到 **“打 Tag 即发布”**：
  - 构建产物在 CI 中统一、可复现；
  - TestPyPI / PyPI 自动接收分发包；
  - 正式发布可以通过 GitHub Environment 手动审批把关。

结合第二篇文档中的 CI workflow，`unifiles` 已经具备一个现代 Python 开源库应有的 **测试 + 构建 + 自动发布** 的完整工程化闭环。随后如果需要，我们还可以写一篇专门讲「版本管理与发布节奏（语义化版本、Changelog、Release Note）」的文档。 
