# 提交并推送到 GitHub（先过本地 CI 再提交）

在提交并推送前，**先本地跑一遍与 `.github/workflows/ci.yml` 一致的检查**（black、mypy、pytest），全部通过后再执行 git 提交与推送。

## 使用方式

- 在 Cursor 命令面板或聊天中触发：
  - `/ci-commit-and-push`

> 如需修改提交信息或分支名，可以在执行命令前，手动编辑下面的命令片段。

## 必做步骤

### 1. 本地执行 CI 检查（与 ci.yml 一致）

**必须先激活项目虚拟环境**，在项目根目录依次执行以下命令。任一步失败则**不要提交**，先修复后再重新执行本命令。

```powershell
chcp 65001
.\.venv\Scripts\Activate.ps1
```

然后按顺序执行与 CI 相同的检查：

```powershell
# 格式检查（与 ci.yml: Run black 一致）
black --check src/ tests/
```

若 black 报错，先执行 `black src/ tests/` 自动格式化，再重新 `black --check`。

```powershell
# 类型检查（与 ci.yml: Run mypy 一致）
mypy src/unifiles/
```

```powershell
# 测试（与 ci.yml: Run tests with pytest 一致）
pytest
```

**仅当以上三步均通过后**，再执行下面的提交与推送。

### 2. 查看当前变更

```powershell
git status
```

### 3. 暂存要提交的文件

- 若本次是 CI 配置相关：
  ```powershell
  git add .github/workflows/ci.yml .gitignore
  ```
- 若有其它本次要提交的文件，一并 add：
  ```powershell
  git add <其它文件路径>
  ```

### 4. 使用中文提交信息进行提交

```powershell
git commit -m "配置 GitHub Actions CI 工作流"
```

（可根据本次变更修改提交信息，例如："修复 tomli 导入警告：添加测试依赖"）

### 5. 推送到远程仓库

- 默认推送到 `origin` 的 `main` 分支：
  ```powershell
  git push origin main
  ```
- 若当前不是 `main`，先查看分支再推送：
  ```powershell
  git branch
  git push origin <当前分支名>
  ```

## 一键执行示例（PowerShell）

在项目根目录的 PowerShell 中，**先确保本地 CI 检查通过**，再执行提交推送。可按以下顺序一次性执行（检查失败时会中断，需先修复再重试）：

```powershell
chcp 65001
.\.venv\Scripts\Activate.ps1
black --check src/ tests/
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
mypy src/unifiles/
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
pytest
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
git status
git add .github/workflows/ci.yml .gitignore
git commit -m "配置 GitHub Actions CI 工作流"
git push origin main
```

执行完成后，到 GitHub 仓库的 **Actions** 标签页，即可看到 CI 工作流开始运行。
