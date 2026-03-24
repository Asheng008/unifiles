#!/usr/bin/env bash
# unifiles - 发布到 PyPI（Linux / macOS）
# 用法：
#   ./publish_pypi.sh test   → 发布到 TestPyPI
#   ./publish_pypi.sh        → 发布到正式 PyPI

set -euo pipefail

# 切换到脚本所在目录（项目根目录）
cd "$(dirname "$0")"

echo "==============================="
echo " unifiles - 发布到 PyPI"
echo " 用法："
echo "   ./publish_pypi.sh test   → 发布到 TestPyPI"
echo "   ./publish_pypi.sh        → 发布到正式 PyPI"
echo "==============================="

# 使用虚拟环境中的 Python
PYTHON=".venv/bin/python"

if [ ! -f "$PYTHON" ]; then
    echo "[错误] 未找到虚拟环境，请先在项目根目录执行："
    echo "  python3 -m venv .venv"
    echo "  source .venv/bin/activate"
    echo "  pip install -e \".[dev]\""
    exit 1
fi

echo ""
echo "[1/4] 升级构建和上传工具（build, twine）..."
"$PYTHON" -m pip install --upgrade build twine

echo ""
echo "[2/4] 清理 dist 目录..."
rm -rf dist

echo ""
echo "[3/4] 构建分发包（sdist + wheel）..."
"$PYTHON" -m build

echo ""
echo "[4/4] 上传到 PyPI..."

if [ "${1:-}" = "test" ]; then
    echo "目標: TestPyPI"
    "$PYTHON" -m twine upload --repository testpypi dist/*
else
    echo "目標: 正式 PyPI"
    "$PYTHON" -m twine upload dist/*
fi

echo ""
echo "[完成] 已成功构建并上传："
ls -lh dist/*.tar.gz dist/*.whl 2>/dev/null
echo ""
if [ "${1:-}" = "test" ]; then
    echo "TestPyPI: https://test.pypi.org/project/unifiles/"
else
    echo "正式 PyPI: https://pypi.org/project/unifiles/"
fi
