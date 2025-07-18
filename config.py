# -*- coding: utf-8 -*-
"""
黄鹏AI对话工具 - 配置文件
请在此文件中配置您的API密钥信息
"""

import os
from typing import Dict, Any

class Config:
    """配置类"""
    
    # ===== Kimi API 配置 =====
    # 请在 https://platform.moonshot.cn/ 获取您的API密钥
    KIMI_API_KEY: str = os.getenv('KIMI_API_KEY', '')
    KIMI_API_URL: str = 'https://api.moonshot.cn/v1/chat/completions'
    KIMI_MODEL: str = 'moonshot-v1-8k'
    
    # ===== 科大讯飞 TTS 配置 =====
    # 请在 https://console.xfyun.cn/ 获取您的API信息
    XFYUN_APPID: str = os.getenv('XFYUN_APPID', '')
    XFYUN_API_KEY: str = os.getenv('XFYUN_API_KEY', '')
    XFYUN_API_SECRET: str = os.getenv('XFYUN_API_SECRET', '')
    
    # ===== 应用配置 =====
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG: bool = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '5000'))
    
    # ===== 对话配置 =====
    MAX_CONVERSATION_HISTORY: int = 20  # 最大对话历史记录数
    MAX_MESSAGE_LENGTH: int = 500  # 最大消息长度
    REQUEST_TIMEOUT: int = 30  # 请求超时时间（秒）
    
    # ===== 语音配置 =====
    VOICE_NAME: str = 'x4_yezi'  # 语音发音人
    AUDIO_FORMAT: str = 'wav'  # 音频格式
    AUDIO_SAMPLE_RATE: int = 16000  # 采样率
    
    # ===== 文件路径配置 =====
    AUDIO_FILES_DIR: str = 'audio_files'  # 音频文件存储目录
    STATIC_DIR: str = 'static'  # 静态文件目录
    TEMPLATES_DIR: str = 'templates'  # 模板文件目录
    
    @classmethod
    def validate(cls) -> Dict[str, Any]:
        """验证配置并返回验证结果"""
        errors = []
        warnings = []
        
        # 检查必需的API密钥
        if not cls.KIMI_API_KEY:
            errors.append("KIMI_API_KEY 未设置")
        
        if not cls.XFYUN_APPID:
            errors.append("XFYUN_APPID 未设置")
            
        if not cls.XFYUN_API_KEY:
            errors.append("XFYUN_API_KEY 未设置")
            
        if not cls.XFYUN_API_SECRET:
            errors.append("XFYUN_API_SECRET 未设置")
        
        # 检查可选配置
        if cls.SECRET_KEY == 'your-secret-key-here':
            warnings.append("建议修改默认的SECRET_KEY")
        
        if cls.DEBUG:
            warnings.append("当前运行在DEBUG模式，生产环境请关闭")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    @classmethod
    def get_config_dict(cls) -> Dict[str, Any]:
        """获取配置字典"""
        return {
            'KIMI_API_KEY': cls.KIMI_API_KEY,
            'KIMI_API_URL': cls.KIMI_API_URL,
            'KIMI_MODEL': cls.KIMI_MODEL,
            'XFYUN_APPID': cls.XFYUN_APPID,
            'XFYUN_API_KEY': cls.XFYUN_API_KEY,
            'XFYUN_API_SECRET': cls.XFYUN_API_SECRET,
            'SECRET_KEY': cls.SECRET_KEY,
            'DEBUG': cls.DEBUG,
            'HOST': cls.HOST,
            'PORT': cls.PORT,
            'MAX_CONVERSATION_HISTORY': cls.MAX_CONVERSATION_HISTORY,
            'MAX_MESSAGE_LENGTH': cls.MAX_MESSAGE_LENGTH,
            'REQUEST_TIMEOUT': cls.REQUEST_TIMEOUT,
            'VOICE_NAME': cls.VOICE_NAME,
            'AUDIO_FORMAT': cls.AUDIO_FORMAT,
            'AUDIO_SAMPLE_RATE': cls.AUDIO_SAMPLE_RATE,
            'AUDIO_FILES_DIR': cls.AUDIO_FILES_DIR,
            'STATIC_DIR': cls.STATIC_DIR,
            'TEMPLATES_DIR': cls.TEMPLATES_DIR,
        }

# 开发环境配置
class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    
# 生产环境配置
class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False

# 根据环境变量选择配置
config_name = os.getenv('FLASK_ENV', 'development')
if config_name == 'production':
    config = ProductionConfig
else:
    config = DevelopmentConfig 
