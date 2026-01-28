# 用户指令记录 (history.md)

本文件按「轮次」记录你发给助手的指令。每轮以「当前对话的简短描述」为标题，下列该轮中的指令。

---

## unifiles 项目规划与文档搭建

### 1. 技术需求文档
> 我想做一个python项目名字叫unifiles，功能是对各种类型的文件读取、写入、抽取、查询，每种类型的文件做一个模块或包，暴露针对这类文件的函数  
> unifiles/  
> ├── pyproject.toml       # 依赖：pandas, openpyxl, pypdf, python-docx  
> └── src/  
>     └── unifiles/  
>         ├── __init__.py  
>         ├── excel.py     # 暴露 read_excel, write_excel, get_sheet_names  
>         ├── pdf.py       # 暴露 extract_text, extract_tables  
>         ├── word.py      # 暴露 read_docx, write_docx  
>         ├── sqlite.py    # 暴露 query, get_schema, get_tables  
>         └── ...          # 其他类型  
> 请写个mvp的技术需求文档

### 2. 修改 AGENTS.md，去掉 MCP 相关内容
> 修改一下 @AGENTS.md 文件，让它专注于文件工具函数的编写，去掉mcp相关的内容

### 3. 保留 MCP 工具体系
> 你搞错我的意思了，它的 mcp 工具体系与调用策略 不要删掉，要保留，这个很重要

### 4. AGENTS.md 推荐 Python 3.9+
> @AGENTS.md 推荐 Python 3.9+ 风格，不管是技术栈，还是类型注解

### 5. 核查 TECH_REQUIREMENTS 的 Python 版本
> 核查@TECH_REQUIREMENTS.md 是否用了 python 3.9+

### 6. 参考 Untitled-1 修改 TECH_REQUIREMENTS
> @TECH_REQUIREMENTS.md 参考@Untitled-1 (31-43) 修改一下

### 7. 修改 AGENTS 依赖库说明
> @AGENTS.md:117-122 这里也改一下

### 8. 编写开发计划
> @TECH_REQUIREMENTS.md @AGENTS.md 根据这两个文件写个开发计划

### 9. 参考 Untitled-1 修改 TECH_REQUIREMENTS（PDF/Excel/依赖锁定）
> @TECH_REQUIREMENTS.md 参考@Untitled-1:29-35 修改一下

### 10. 参考 Untitled-1 修改 DEVELOPMENT_PLAN（CI/CD、Pre-commit）
> 参考 @Untitled-1:29-35 修改 @DEVELOPMENT_PLAN.md

### 11. 编写 README
> 为本项目写个readme文档

### 12. 编写 Cursor 命令（更新 README）
> 写个 cursor的command 用来更新readme文档，不清楚怎么写的话，可以联网查一下，或参考cursor官方文档

### 13. 创建 history.md
> 一个 history.md

### 14. 新建 history.md 并记录本轮所有指令
> 新建一个 history.md 文件，用来记录我发给你的指令，现在把这一轮对话我所有的指令记录下来

---

## 使用说明

- 之后可在本文件末尾按时间顺序追加新的指令。
- 建议每条保留原始表述（或重要片段），必要时可加一行“结果/产物”简记（如：已生成 `TECH_REQUIREMENTS.md`）。
