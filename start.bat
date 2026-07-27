@echo off
chcp 65001 >/dev/null 2>&1
title "Python 学习计划 - Web 阅读程序"

echo ================================================
echo   "Python 学习计划 - Web 阅读程序"
echo ================================================
echo.

python --version >/dev/null 2>&1
if %errorlevel% neq 0 (
    echo "[错误] 未找到 Python，请先安装 Python 3.10+"
    echo "下载地址：https://www.python.org/downloads/"
    pause
    exit /b 1
)

echo "[信息] 正在安装依赖包..."
pip install flask mistune -q

echo.
echo "[信息] 正在启动 Web 服务器..."
echo "[信息] 访问地址：http://localhost:5000"
echo "[信息] 按 Ctrl+C 停止服务"
echo.

python server.py
pause
