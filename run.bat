@echo off
chcp 65001
echo ============================================================
echo 🎉 黄鹏AI对话工具 - Windows启动脚本
echo 💝 专为谢猪猪定制的AI小伙伴
echo ============================================================
echo.

echo 📍 当前目录: %CD%
echo.

echo 🔍 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未安装或未添加到PATH
    echo 💡 请先安装Python 3.7+
    pause
    exit /b 1
)

echo ✅ Python环境检查通过
echo.

echo 🚀 启动黄鹏AI对话工具...
echo 💡 如果出现错误，请检查config.py中的API密钥配置
echo.

python start.py

echo.
echo 👋 程序已退出
pause 