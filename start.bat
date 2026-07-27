@echo off
chcp 65001 >nul 2>&1
title "Python 学习计划 - Web 阅读程序"

echo ================================================
echo   "Python 学习计划 - Web 阅读程序"
echo ================================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo "[错误] 未找到 Python，请先安装 Python 3.10+"
    echo "下载地址：https://www.python.org/downloads/"
    pause
    exit /b 1
)

REM 检查依赖包是否已安装
python -c "import flask, mistune" >nul 2>&1
if %errorlevel% neq 0 (
    echo "[信息] 正在安装依赖包..."
    pip install flask mistune -q
    if %errorlevel% neq 0 (
        echo "[错误] 依赖包安装失败"
        echo "请用镜像源尝试：pip install flask mistune -i https://mirrors.aliyun.com/pypi/simple/"
        pause
        exit /b 1
    )
) else (
    echo "[信息] 依赖包已就绪"
)

echo.
echo "[信息] 正在启动 Web 服务器..."
echo "[信息] 访问地址：http://localhost:5000"
echo "[信息] 按 Ctrl+C 停止服务"
echo.

python server.py
pause
