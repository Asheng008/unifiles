# 提交 CI 配置并推送到 GitHub

为当前项目的一整套「CI 配置提交与推送」流程提供一键命令，确保：

- 将 `.github/workflows/ci.yml` 和相关文件提交到 Git 仓库
- 使用 **中文提交信息**
- 推送到远程分支，让 GitHub Actions 自动开始运行 CI

## 使用方式

- 在 Cursor 命令面板或聊天中触发：
  - `/ci-commit-and-push`

> 如需修改提交信息或分支名，可以在执行命令前，手动编辑下面的命令片段。

## 必做步骤

1. **查看当前变更**
   - 在项目根目录执行：
   ```powershell
   chcp 65001
   git status
   ```

2. **暂存与 CI 配置相关的文件**
   - 至少包括：
   ```powershell
   git add .github/workflows/ci.yml .gitignore
   ```
   - 如果还修改了其它与本次提交相关的文件，也可以一起 add：
   ```powershell
   git add <其它文件路径>
   ```

3. **使用中文提交信息进行提交**
   - 推荐使用如下中文提交信息（可根据需要调整）：
   ```powershell
   git commit -m "配置 GitHub Actions CI 工作流"
   ```

4. **推送到远程仓库**
   - 默认推送到 `origin` 的 `main` 分支：
   ```powershell
   git push origin main
   ```
   - 如果当前不是 `main` 分支，请将 `main` 替换为实际分支名：
   ```powershell
   git branch    # 查看当前分支
   git push origin <当前分支名>
   ```

## 一键执行示例（PowerShell）

在项目根目录的 PowerShell 中，可以按以下顺序一次性执行（如适用于当前分支和变更范围）：

```powershell
chcp 65001
git status
git add .github/workflows/ci.yml .gitignore
git commit -m "配置 GitHub Actions CI 工作流"
git push origin main
```

执行完成后，到 GitHub 仓库的 **Actions** 标签页，即可看到 CI 工作流开始运行。
