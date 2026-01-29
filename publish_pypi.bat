@echo off
setlocal

rem 切换到脚本所在目录（项目根目录）
cd /d "%~dp0"

rem 设置控制台为 UTF-8，避免中文输出乱码
chcp 65001 >NUL

echo ===============================
echo  unifiles - 发布到 PyPI
echo  用法：
echo    publish_pypi.bat test   ^> 发布到 TestPyPI
echo    publish_pypi.bat        ^> 发布到正式 PyPI
echo ===============================

rem 使用虚拟环境中的 Python
set "PYTHON=.venv\Scripts\python.exe"

if not exist "%PYTHON%" (
    echo [错误] 未找到虚拟环境，请先在项目根目录执行：
    echo   python -m venv .venv
    echo   .\.venv\Scripts\Activate.ps1
    echo   pip install -e ".[dev]"
    exit /b 1
)

echo.
echo [1/4] 升级构建和上传工具（build, twine）...
"%PYTHON%" -m pip install --upgrade build twine
if errorlevel 1 (
    echo [错误] 安装/升级 build, twine 失败。
    exit /b 1
)

echo.
echo [2/4] 清理 dist 目录...
if exist "dist" (
    rmdir /s /q "dist"
)

echo.
echo [3/4] 构建分发包（sdist + wheel）...
"%PYTHON%" -m build
if errorlevel 1 (
    echo [错误] 构建失败，请检查 pyproject.toml 配置和代码。
    exit /b 1
)

echo.
echo [4/4] 上传到 PyPI...

if /I "%1"=="test" (
    echo 目標: TestPyPI
    "%PYTHON%" -m twine upload --repository testpypi dist\*
) else (
    echo 目標: 正式 PyPI
    "%PYTHON%" -m twine upload dist\*
)

if errorlevel 1 (
    echo [错误] 上传失败，请检查网络、凭证或版本号是否重复。
    exit /b 1
)

echo.
echo [完成] 已成功构建并上传：
echo   dist\unifiles-0.1.0*.tar.gz
echo   dist\unifiles-0.1.0*-py3-none-any.whl
echo.
echo 如果是 TestPyPI，可访问：
echo   https://test.pypi.org/project/unifiles/
echo 如果是正式 PyPI，可访问：
echo   https://pypi.org/project/unifiles/

endlocal
exit /b 0
