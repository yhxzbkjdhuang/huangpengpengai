#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄鹏AI对话工具 - 启动脚本
"""

import os
import sys
import subprocess
import webbrowser
import time
from config import config

def check_dependencies():
    """检查依赖包是否安装"""
    print("🔍 检查依赖包...")
    
    try:
        import flask
        import flask_cors
        import requests
        import websocket
        print("✅ 所有依赖包已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("📦 请运行以下命令安装依赖:")
        print("   pip install -r requirements.txt")
        return False

def check_config():
    """检查配置"""
    print("🔍 检查配置...")
    
    validation = config.validate()
    
    if validation['valid']:
        print("✅ 配置检查通过")
        
        if validation['warnings']:
            print("⚠️  配置警告:")
            for warning in validation['warnings']:
                print(f"   - {warning}")
        
        return True
    else:
        print("❌ 配置检查失败:")
        for error in validation['errors']:
            print(f"   - {error}")
        
        print("\n📝 配置说明:")
        print("1. 编辑 config.py 文件")
        print("2. 填入您的API密钥:")
        print("   - KIMI_API_KEY: 在 https://platform.moonshot.cn/ 获取")
        print("   - XFYUN_APPID, XFYUN_API_KEY, XFYUN_API_SECRET: 在 https://console.xfyun.cn/ 获取")
        
        return False

def create_directories():
    """创建必要的目录"""
    print("📁 创建必要目录...")
    
    directories = [
        config.AUDIO_FILES_DIR,
        config.STATIC_DIR,
        config.TEMPLATES_DIR
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✅ {directory}")

def print_banner():
    """打印启动横幅"""
    print("=" * 60)
    print("🎉 黄鹏AI对话工具")
    print("💝 专为谢猪猪定制的AI小伙伴")
    print("=" * 60)
    print()

def print_startup_info():
    """打印启动信息"""
    print("🚀 启动信息:")
    print(f"   📱 访问地址: http://{config.HOST}:{config.PORT}")
    print(f"   🔧 调试模式: {'开启' if config.DEBUG else '关闭'}")
    print(f"   🗣️  语音发音人: {config.VOICE_NAME}")
    print(f"   📝 最大消息长度: {config.MAX_MESSAGE_LENGTH}字符")
    print()

def open_browser():
    """打开浏览器"""
    url = f"http://localhost:{config.PORT}"
    
    print(f"🌐 正在打开浏览器: {url}")
    
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"❌ 无法自动打开浏览器: {e}")
        print(f"💡 请手动在浏览器中访问: {url}")
        return False

def start_server():
    """启动服务器"""
    print("🔥 启动服务器...")
    print("💡 按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    try:
        # 导入并运行Flask应用
        from app import app
        
        # 延迟打开浏览器
        if not config.DEBUG:
            import threading
            def delayed_open():
                time.sleep(2)
                open_browser()
            threading.Thread(target=delayed_open, daemon=True).start()
        
        # 启动Flask应用
        app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG,
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

def main():
    """主函数"""
    print_banner()
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 检查配置
    if not check_config():
        sys.exit(1)
    
    # 创建目录
    create_directories()
    
    # 打印启动信息
    print_startup_info()
    
    # 启动服务器
    start_server()

if __name__ == "__main__":
    main() 