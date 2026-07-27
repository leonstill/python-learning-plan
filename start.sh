#!/usr/bin/env bash
# -*- coding: utf-8 -*-
set -e

echo "================================================"
echo "  Python 学习计划 - Web 阅读程序"
echo "================================================"
echo ""

# 检查 Python
if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    echo "[错误] 未找到 Python，请先安装 Python 3.10+"
    echo "下载地址：https://www.python.org/downloads/"
    exit 1
fi

PYTHON=$(command -v python3 || command -v python)

# 检查依赖包
if ! $PYTHON -c "import flask, mistune" 2>/dev/null; then
    echo "[信息] 正在安装依赖包..."
    pip install flask mistune -q
    if [ $? -ne 0 ]; then
        echo "[错误] 依赖包安装失败"
        echo "请用镜像源尝试：pip install flask mistune -i https://mirrors.aliyun.com/pypi/simple/"
        exit 1
    fi
else
    echo "[信息] 依赖包已就绪"
fi

echo ""
echo "[信息] 正在启动 Web 服务器..."
echo "[信息] 访问地址：http://localhost:5000"
echo "[信息] 按 Ctrl+C 停止服务"
echo ""

$PYTHON server.py
