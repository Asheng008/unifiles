# 更新 README 文档

根据项目当前状态更新 `README.md`，使其与需求文档、开发计划和实际代码保持一致。

## 目标

- 更新 README.md，确保内容与 TECH_REQUIREMENTS.md、DEVELOPMENT_PLAN.md、AGENTS.md 及当前代码/目录一致
- 保持现有 README 的结构、语气（中文）和排版风格
- 不改变文档的整体章节顺序，只增删改必要内容

## 必做步骤

1. **读取项目文档（按需引用）**
   - `TECH_REQUIREMENTS.md`：功能范围、API 设计、使用示例、环境与依赖
   - `DEVELOPMENT_PLAN.md`：阶段与里程碑、项目结构
   - `AGENTS.md`：技术栈、类型注解与规范（仅在与 README 描述相关时参考）
   - 当前 `README.md`：作为「要更新的文件」的基准

2. **核对并更新以下部分**
   - **特性**：若项目定位或卖点有变化，与 TECH_REQUIREMENTS 一致即可
   - **支持的文件类型**：表格与 TECH_REQUIREMENTS 第 2.1 节一致；若有 PDF/Excel 等限制说明，保留或补充
   - **环境要求**：Python 版本、操作系统与 TECH_REQUIREMENTS 第 11 节一致
   - **安装**：若已存在 `pyproject.toml`，安装说明要能真实执行；仓库地址可保留占位或按实际填写
   - **快速开始 / API 概览**：函数名、参数、返回值、示例代码与 TECH_REQUIREMENTS 第 4、6 节及 `src/unifiles/` 下实现一致；若有新模块或新函数，补充对应小节与示例
   - **项目结构**：与当前仓库目录树一致（含 `.cursor`、`src/unifiles`、`tests` 等）
   - **开发与贡献**：所引用的文档路径、命令（如 PowerShell）与 DEVELOPMENT_PLAN、AGENTS 一致

3. **约束**
   - 使用中文撰写，语气保持说明性、简洁
   - 代码块语言标记正确（如 `bash`、`python`）
   - 表格、列表、引用块格式与原 README 风格一致，不引入多余层级

## 输出

- 直接修改并保存 `README.md`
- 若某章节因「暂无实现/暂无文档」无法更新，在该处加一句简短说明（如「待实现」），并保持章节存在，便于后续补全
