#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
黄鹏AI对话工具 - 系统测试脚本
用于验证各项功能是否正常工作
"""

import requests
import json
import time
import os
import sys
from config import config

def test_server_status():
    """测试服务器状态"""
    print("=" * 50)
    print("🚀 测试服务器状态...")
    
    # 使用localhost地址而不是配置中的0.0.0.0
    test_host = '127.0.0.1' if config.HOST == '0.0.0.0' else config.HOST
    
    try:
        response = requests.get(f'http://{test_host}:{config.PORT}/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 服务器状态: {data['status']}")
            print(f"📝 消息: {data['message']}")
            print(f"🔢 版本: {data['version']}")
            return True
        else:
            print(f"❌ 服务器响应异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到服务器: {e}")
        return False

def test_system_components():
    """测试系统组件状态"""
    print("\n" + "=" * 50)
    print("🔧 测试系统组件...")
    
    # 使用localhost地址而不是配置中的0.0.0.0
    test_host = '127.0.0.1' if config.HOST == '0.0.0.0' else config.HOST
    
    try:
        response = requests.get(f'http://{test_host}:{config.PORT}/test', timeout=5)
        if response.status_code == 200:
            status = response.json()
            
            components = {
                'flask': 'Flask服务',
                'config': '配置管理',
                'tts_service': 'TTS语音合成',
                'asr_service': 'ASR语音识别',
                'ffmpeg': 'FFmpeg音频处理'
            }
            
            working_count = 0
            total_count = len(components)
            
            for key, name in components.items():
                if status.get(key, False):
                    print(f"✅ {name}: 正常")
                    working_count += 1
                else:
                    print(f"❌ {name}: 异常")
            
            print(f"\n📊 组件状态: {working_count}/{total_count} 正常")
            
            if working_count >= 4:  # FFmpeg是可选的
                print("🎉 核心组件运行正常！")
                return True
            else:
                print("⚠️ 部分核心组件异常，请检查配置")
                return False
                
        else:
            print(f"❌ 组件检查失败: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 组件检查异常: {e}")
        return False

def test_chat_functionality():
    """测试对话功能"""
    print("\n" + "=" * 50)
    print("💬 测试对话功能...")
    
    # 使用localhost地址而不是配置中的0.0.0.0
    test_host = '127.0.0.1' if config.HOST == '0.0.0.0' else config.HOST
    
    try:
        test_message = "你好，黄鹏！"
        
        response = requests.post(
            f'http://{test_host}:{config.PORT}/chat',
            json={
                'message': test_message,
                'history': []
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                print(f"✅ 对话功能正常")
                print(f"📝 测试消息: {test_message}")
                print(f"🤖 AI回复: {data['response'][:100]}...")
                return True
            else:
                print(f"❌ 对话返回错误: {data.get('error', '未知错误')}")
                return False
        else:
            print(f"❌ 对话请求失败: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 对话功能异常: {e}")
        return False

def test_tts_functionality():
    """测试语音合成功能"""
    print("\n" + "=" * 50)
    print("🔊 测试语音合成功能...")
    
    # 使用localhost地址而不是配置中的0.0.0.0
    test_host = '127.0.0.1' if config.HOST == '0.0.0.0' else config.HOST
    
    try:
        test_text = "你好，谢猪猪！"
        
        response = requests.post(
            f'http://{test_host}:{config.PORT}/synthesize',
            json={'text': test_text},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                print(f"✅ 语音合成功能正常")
                print(f"📝 测试文本: {test_text}")
                print(f"🎵 音频URL: {data['audio_url']}")
                return True
            else:
                print(f"❌ 语音合成返回错误: {data.get('error', '未知错误')}")
                return False
        else:
            print(f"❌ 语音合成请求失败: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 语音合成功能异常: {e}")
        return False

def test_config_validation():
    """测试配置验证"""
    print("\n" + "=" * 50)
    print("⚙️ 测试配置验证...")
    
    try:
        validation = config.validate()
        
        if validation['valid']:
            print("✅ 配置验证通过")
            
            if validation['warnings']:
                print("⚠️ 配置警告:")
                for warning in validation['warnings']:
                    print(f"   - {warning}")
            
            return True
        else:
            print("❌ 配置验证失败:")
            for error in validation['errors']:
                print(f"   - {error}")
            return False
            
    except Exception as e:
        print(f"❌ 配置验证异常: {e}")
        return False

def test_file_structure():
    """测试文件结构"""
    print("\n" + "=" * 50)
    print("📁 测试文件结构...")
    
    required_files = [
        'app.py',
        'config.py',
        'tts_service.py',
        'asr_service.py',
        'requirements.txt',
        'templates/index.html',
        'static/css/style.css',
        'static/js/chat.js'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - 文件缺失")
            missing_files.append(file_path)
    
    if not missing_files:
        print("🎉 所有必需文件都存在！")
        return True
    else:
        print(f"⚠️ 缺失 {len(missing_files)} 个文件")
        return False

def main():
    """主测试函数"""
    print("🎯 黄鹏AI对话工具 - 系统测试")
    print("=" * 50)
    
    tests = [
        ("文件结构", test_file_structure),
        ("配置验证", test_config_validation),
        ("服务器状态", test_server_status),
        ("系统组件", test_system_components),
        ("对话功能", test_chat_functionality),
        ("语音合成", test_tts_functionality),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    # 显示测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📈 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常！")
        return True
    elif passed >= total * 0.8:
        print("⚠️ 大部分测试通过，系统基本可用")
        return True
    else:
        print("❌ 多项测试失败，请检查系统配置")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 