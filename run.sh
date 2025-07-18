#!/bin/bash

# 设置颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "============================================================"
echo "🎉 黄鹏AI对话工具 - Linux/Mac启动脚本"
echo "💝 专为谢猪猪定制的AI小伙伴"
echo "============================================================"
echo

echo "📍 当前目录: $(pwd)"
echo

echo "🔍 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3未安装${NC}"
    echo "💡 请先安装Python 3.7+"
    exit 1
fi

echo -e "${GREEN}✅ Python环境检查通过${NC}"
echo

echo "🚀 启动黄鹏AI对话工具..."
echo "💡 如果出现错误，请检查config.py中的API密钥配置"
echo

python3 start.py

echo
echo "👋 程序已退出" 