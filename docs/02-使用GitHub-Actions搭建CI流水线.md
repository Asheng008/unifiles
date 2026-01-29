# 技术文档（二）：使用 GitHub Actions 为 unifiles 搭建 CI 流水线

本文介绍如何为 `unifiles` 项目配置一套 **GitHub Actions CI 流水线**，在每次提交或 Pull Request 时自动完成：

- 安装依赖
- 代码格式检查（`black --check`）
- 类型检查（`mypy`）
- 单元测试与覆盖率（`pytest`）
- 构建分发包（`python -m build`）

并为后续「自动发布到 PyPI」打好基础。内容结合了 GitHub 官方文档和 Python Packaging 官方指南的最佳实践设计。

---

## 1. GitHub Actions 基本概念

- **工作流（workflow）**：一个 `.yml` 文件，放在仓库 `.github/workflows/` 目录下。
- **触发器（on）**：何时触发，例如 `push`、`pull_request`、`workflow_dispatch`（手动触发）等。
- **Job**：工作流中的一个“任务单元”，可以并行或串行执行。
- **Step**：Job 内的具体步骤，比如“检出代码”“安装 Python”“运行 pytest”。
- **Runner**：实际执行 Job 的机器，一般使用 GitHub 托管的 `ubuntu-latest`。

对于 `unifiles` 这种纯 Python 库，推荐做两套工作流：

- 一个 **CI 工作流**：在 push / PR 时跑测试、类型检查、格式检查、构建。
- 一个 **发布工作流**（后续可加）：打 Tag 或发布 Release 时自动发布到 PyPI。

本文重点讲 **CI 工作流**。

---

## 2. CI 的最佳实践要点（结合官方推荐）

综合 GitHub 官方文档和 Python Packaging 用户指南，适合本项目的最佳实践包括：

- **多 Python 版本测试（matrix）**：
  - 使用 `actions/setup-python` + `strategy.matrix`，在 3.9 / 3.10 / 3.11 / 3.12 下跑测试，确保兼容性。
- **依赖缓存（cache）**：
  - 使用 `actions/cache` 对 `pip` 缓存目录做缓存，加速重复构建。
- **分阶段步骤清晰**：
  - 明确区分：安装依赖 → 代码质量检查（black/mypy）→ 测试（pytest）→ 构建（build）。
- **最小权限原则**：
  - 默认使用 `GITHUB_TOKEN`，只授予必要的权限；纯 CI 工作流一般不需要额外写权限。
- **失败快速反馈**：
  - 所有检查失败时直接 Fail，让问题在 PR 阶段就暴露出来。
- **与本地命令保持一致**：
  - 工作流中用的命令尽量与 `README.md` / `TECH_REQUIREMENTS.md` / 本地开发命令相同（如 `pytest tests/ -v`、`mypy src/unifiles/`、`black --check src/ tests/`）。

---

## 3. 创建 CI 工作流文件

在仓库中新建目录和文件：

```text
.github/
└── workflows/
    └── ci.yml
```

### 3.1 完整示例：`ci.yml`

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    name: Test on Python ${{ matrix.python-version }}
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: "pip"

      - name: Install dependencies (including dev)
        run: |
          python -m pip install --upgrade pip
          python -m pip install build
          # 安装项目本身及开发依赖，相当于本地的 `pip install -e ".[dev]"`
          pip install -e ".[dev]"

      - name: Run black (format check)
        run: |
          black --check src/ tests/

      - name: Run mypy (type check)
        run: |
          mypy src/unifiles/

      - name: Run tests with pytest
        run: |
          pytest tests/ -v

      - name: Build distributions
        run: |
          python -m build
```

### 3.2 关键点说明

- **触发条件**：
  - 对 `main` 分支的 `push` 和 `pull_request` 自动触发。
- **矩阵测试**：
  - 在 3.9 / 3.10 / 3.11 / 3.12 上各跑一遍，符合 `pyproject.toml` 中声明的支持版本。
- **依赖安装**：
  - 先 `pip install build`，再 `pip install -e ".[dev]"`，与本地推荐用法一致。
- **黑盒构建验证**：
  - CI 中也跑一遍 `python -m build`，确保任何改动都不会破坏打包过程。
- **缓存 pip**（通过 `setup-python` 的 `cache: "pip"`）：
  - GitHub 官方推荐的方式，比自己手写 `actions/cache` 更简单。

---

## 4. 分离测试与构建（可选优化）

如果希望结构更清晰，可以拆成两个 Job：

- `lint_and_test`：black + mypy + pytest
- `build`：依赖 `lint_and_test` 成功后再构建分发包

示例结构（简化版）：

```yaml
jobs:
  lint_and_test:
    runs-on: ubuntu-latest
    # ... 同上，跑 black/mypy/pytest ...

  build:
    needs: lint_and_test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"
      - name: Install build deps
        run: |
          python -m pip install --upgrade pip
          pip install build
          pip install -e ".[dev]"
      - name: Build distributions
        run: python -m build
      - name: Upload dist artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/*
```

这样可以方便后续在 `build` 的基础上再接一个「发布到 PyPI」的工作流。

---

## 5. 与发布流程的衔接建议

当前你已经有本地批处理脚本 `publish_pypi.bat` 和 Cursor 命令用于发布。结合官方推荐做法，CI 与发布可以这样协同：

- **CI（ci.yml，本篇已介绍）**：
  - 任何 push / PR → 自动质量检查（black/mypy/pytest）+ 构建验证。
- **发布（单独的 workflow，例如 `publish.yml`，后续文档可详细写）**：
  - 触发条件可以是：
    - 打 Tag：`on: push: tags: ["v*"]`
    - 创建 Release：`on: release: types: [published]`
  - 使用官方推荐的 `pypa/gh-action-pypi-publish` Action：
    - TestPyPI：先发到测试仓库
    - 正式 PyPI：测试通过后再发正式

粗略示意（仅展示大致结构）：

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - "v*"

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install build
        run: |
          python -m pip install --upgrade pip
          pip install build
      - name: Build
        run: python -m build
      - name: Publish package
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

> 官方推荐：使用 `pypa/gh-action-pypi-publish` 作为发布到 PyPI 的「官方 Action」，并通过仓库 Secret（如 `PYPI_API_TOKEN`）注入凭证，避免在工作流中写死 Token。

---

## 6. 小结：在 unifiles 项目中的落地步骤

1. 在仓库中创建 `.github/workflows/ci.yml`，内容参考第 3 节完整示例。
2. 提交并推送到 GitHub 后，进入仓库的 **Actions** 标签页，确认 CI 能自动跑起来。
3. 确认 CI 中的 Python 版本矩阵、命令（black/mypy/pytest/build）与本地文档一致。
4. 后续可以新增一个 `publish.yml`，用来在打 Tag 时自动发布到 PyPI，与当前的本地批处理脚本/技术文档形成互补。

这样，`unifiles` 在 **质量保障（CI）** 和 **发布流程（CD）** 上就都具备了现代 Python 项目推荐的工程化基础。后续如果你愿意，我们可以在第三篇文档里专门写「用 GitHub Actions 自动发布到 TestPyPI / PyPI」。
