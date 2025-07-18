@echo off
chcp 65001 > nul
title 黄鹏AI对话工具 - 快速启动

echo.
echo ==========================================
echo 🎉 黄鹏AI对话工具 - 快速启动
echo 💝 专为谢猪猪定制的AI小伙伴
echo ==========================================
echo.

echo 🚀 正在启动服务器...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未安装或不在PATH中
    echo 请先安装Python 3.7或更高版本
    pause
    exit /b 1
)

REM 检查依赖包
echo 🔍 检查依赖包...
python -c "import flask, requests, websocket" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ 正在安装依赖包...
    pip install -r requirements.txt
)

REM 启动服务器
echo 🔥 启动服务器...
echo 💡 浏览器将自动打开，请稍等...
echo.

REM 在后台启动Python服务器
start /b python start.py

REM 等待服务器启动
timeout /t 3 /nobreak >nul

REM 打开浏览器
start http://127.0.0.1:5000

echo.
echo ✅ 服务器已启动！
echo 📱 访问地址: http://127.0.0.1:5000
echo 💡 按 Ctrl+C 停止服务器
echo.

REM 保持窗口打开
pause 