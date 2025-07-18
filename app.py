from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import requests
import json
import os
import tempfile
import time
import base64
import io
import wave
from tts_service import TTSService
from asr_service import ASRService
import logging
from config import config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 从配置文件获取配置
app.config.from_object(config)

# 验证配置
config_validation = config.validate()
if not config_validation['valid']:
    logger.error("配置验证失败:")
    for error in config_validation['errors']:
        logger.error(f"  - {error}")
    exit(1)

if config_validation['warnings']:
    logger.warning("配置警告:")
    for warning in config_validation['warnings']:
        logger.warning(f"  - {warning}")

# 初始化TTS服务
tts_service = TTSService(
    config.XFYUN_APPID,
    config.XFYUN_API_KEY,
    config.XFYUN_API_SECRET
)

# 初始化ASR服务
asr_service = ASRService(
    config.XFYUN_APPID,
    config.XFYUN_API_KEY,
    config.XFYUN_API_SECRET
)

# 黄鹏的个性化设定
HUANG_PENG_PERSONA = """
你是黄鹏，一个风趣幽默的男生，是谢猪猪的专属AI小伙伴。
你的特点：
1. 总是称呼用户为"谢猪猪"
2. 说话风格轻松幽默，但不失贴心
3. 经常用一些可爱的词汇和表情
4. 偶尔会开一些无伤大雅的小玩笑
5. 对谢猪猪很关心，会主动询问她的感受
6. 喜欢讲有趣的故事和笑话
7. 说话时会用一些网络用语，但不过分
请记住你是黄鹏，要保持这个角色设定，每次回答都要体现出你对谢猪猪的关心和幽默感。
"""

def call_kimi_api(message, conversation_history=[]):
    """调用Kimi API进行对话"""
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {config.KIMI_API_KEY}'
        }
        
        messages = [
            {"role": "system", "content": HUANG_PENG_PERSONA},
        ]
        
        # 添加历史对话
        messages.extend(conversation_history)
        
        # 添加当前消息
        messages.append({"role": "user", "content": message})
        
        data = {
            "model": config.KIMI_MODEL,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(
            config.KIMI_API_URL,
            headers=headers,
            json=data,
            timeout=config.REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            logger.error(f"Kimi API error: {response.status_code}, {response.text}")
            return "哎呀，谢猪猪，我的大脑有点卡住了，稍等一下再聊吧~"
            
    except Exception as e:
        logger.error(f"调用Kimi API失败: {str(e)}")
        return "哎呀，谢猪猪，我好像遇到了一点小问题，但我还是很想和你聊天的！"

def convert_webm_to_pcm(webm_data):
    """将WebM音频数据转换为PCM格式"""
    try:
        logger.info("开始转换WebM音频格式")
        
        # 检查是否安装了ffmpeg
        import subprocess
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            logger.info("FFmpeg已安装")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("FFmpeg未安装或不可用")
            # 尝试直接使用原始数据
            return webm_data
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as webm_file:
            webm_file.write(webm_data)
            webm_path = webm_file.name
        
        logger.info(f"临时WebM文件: {webm_path}")
        
        # 使用ffmpeg转换为PCM格式
        pcm_path = webm_path.replace('.webm', '.pcm')
        
        cmd = [
            'ffmpeg', '-i', webm_path,
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-ac', '1',
            '-f', 's16le',
            '-y',  # 覆盖输出文件
            pcm_path
        ]
        
        logger.info(f"FFmpeg命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"FFmpeg转换失败: {result.stderr}")
            # 清理临时文件
            try:
                os.unlink(webm_path)
            except:
                pass
            return None
        
        # 检查PCM文件是否存在
        if not os.path.exists(pcm_path):
            logger.error(f"PCM文件未生成: {pcm_path}")
            os.unlink(webm_path)
            return None
        
        # 读取PCM数据
        with open(pcm_path, 'rb') as pcm_file:
            pcm_data = pcm_file.read()
        
        logger.info(f"PCM数据大小: {len(pcm_data)} bytes")
        
        # 清理临时文件
        try:
            os.unlink(webm_path)
            os.unlink(pcm_path)
        except Exception as e:
            logger.warning(f"清理临时文件失败: {str(e)}")
        
        return pcm_data
        
    except Exception as e:
        logger.error(f"音频转换异常: {str(e)}", exc_info=True)
        return None

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """处理对话请求"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '请求数据格式错误'}), 400
            
        message = data.get('message', '')
        history = data.get('history', [])
        
        if not message:
            return jsonify({'error': '消息不能为空'}), 400
            
        if len(message) > config.MAX_MESSAGE_LENGTH:
            return jsonify({'error': f'消息长度不能超过{config.MAX_MESSAGE_LENGTH}字符'}), 400
        
        # 调用Kimi API获取回复
        response = call_kimi_api(message, history)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"处理对话请求失败: {str(e)}")
        return jsonify({'error': '处理请求失败'}), 500

@app.route('/recognize', methods=['POST'])
def recognize():
    """语音识别接口"""
    try:
        logger.info("收到语音识别请求")
        
        # 检查是否有文件上传
        if 'audio' not in request.files:
            logger.error("没有音频文件")
            return jsonify({'error': '没有音频文件'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            logger.error("没有选择音频文件")
            return jsonify({'error': '没有选择音频文件'}), 400
        
        logger.info(f"接收到音频文件: {audio_file.filename}, 类型: {audio_file.content_type}")
        
        # 读取音频数据
        audio_data = audio_file.read()
        logger.info(f"音频数据大小: {len(audio_data)} bytes")
        
        # 检查音频数据大小
        if len(audio_data) > 5 * 1024 * 1024:  # 5MB限制
            logger.error("音频文件太大")
            return jsonify({'error': '音频文件太大'}), 400
        
        # 检查音频数据是否为空
        if len(audio_data) == 0:
            logger.error("音频数据为空")
            return jsonify({'error': '音频数据为空'}), 400
        
        # 转换音频格式（如果需要）
        if audio_file.content_type == 'audio/webm':
            logger.info("开始转换WebM格式音频")
            pcm_data = convert_webm_to_pcm(audio_data)
            if not pcm_data:
                logger.error("音频格式转换失败，尝试直接使用原始数据")
                # 如果转换失败，尝试直接使用原始数据
                pcm_data = audio_data
        else:
            logger.info("直接使用原始音频数据")
            pcm_data = audio_data
        
        logger.info(f"处理后的音频数据大小: {len(pcm_data)} bytes")
        
        # 检查ASR服务是否初始化
        if not asr_service:
            logger.error("ASR服务未初始化")
            return jsonify({'error': 'ASR服务未初始化'}), 500
        
        # 调用ASR服务
        logger.info("开始调用ASR服务")
        recognition_result = asr_service.recognize(pcm_data)
        
        if recognition_result:
            logger.info(f"识别结果: {recognition_result}")
            return jsonify({
                'text': recognition_result,
                'status': 'success'
            })
        else:
            logger.error("ASR服务返回空结果")
            return jsonify({'error': '语音识别失败，请确保音频清晰并重试'}), 500
            
    except Exception as e:
        logger.error(f"语音识别异常: {str(e)}", exc_info=True)
        return jsonify({'error': f'语音识别异常: {str(e)}'}), 500

@app.route('/synthesize', methods=['POST'])
def synthesize():
    """语音合成接口"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '请求数据格式错误'}), 400
            
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': '文本不能为空'}), 400
            
        if len(text) > config.MAX_MESSAGE_LENGTH:
            return jsonify({'error': f'文本长度不能超过{config.MAX_MESSAGE_LENGTH}字符'}), 400
        
        # 调用TTS服务
        audio_file = tts_service.synthesize(text)
        
        if audio_file:
            return jsonify({
                'audio_url': f'/audio/{os.path.basename(audio_file)}',
                'status': 'success'
            })
        else:
            return jsonify({'error': '语音合成失败'}), 500
            
    except Exception as e:
        logger.error(f"语音合成失败: {str(e)}")
        return jsonify({'error': '语音合成失败'}), 500

@app.route('/audio/<filename>')
def serve_audio(filename):
    """提供音频文件"""
    try:
        # 安全检查：只允许访问音频文件目录中的文件
        if not filename.endswith('.wav'):
            return jsonify({'error': '不支持的文件格式'}), 400
            
        audio_path = os.path.join(config.AUDIO_FILES_DIR, filename)
        
        # 检查文件是否在允许的目录中
        if not os.path.abspath(audio_path).startswith(os.path.abspath(config.AUDIO_FILES_DIR)):
            return jsonify({'error': '非法访问'}), 403
            
        if os.path.exists(audio_path):
            return send_file(audio_path, mimetype='audio/wav')
        else:
            return jsonify({'error': '音频文件不存在'}), 404
    except Exception as e:
        logger.error(f"提供音频文件失败: {str(e)}")
        return jsonify({'error': '提供音频文件失败'}), 500

@app.route('/test', methods=['GET'])
def test_status():
    """测试系统状态"""
    try:
        status = {
            'flask': True,
            'config': True,
            'tts_service': False,
            'asr_service': False,
            'ffmpeg': False
        }
        
        # 检查TTS服务
        try:
            if tts_service:
                status['tts_service'] = True
        except Exception as e:
            logger.error(f"TTS服务检查失败: {str(e)}")
        
        # 检查ASR服务
        try:
            if asr_service:
                status['asr_service'] = True
        except Exception as e:
            logger.error(f"ASR服务检查失败: {str(e)}")
        
        # 检查FFmpeg
        try:
            import subprocess
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            status['ffmpeg'] = True
        except:
            pass
        
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"系统状态检查失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy', 
        'message': '黄鹏AI对话工具运行正常',
        'version': '1.0.0',
        'features': {
            'tts': True,
            'asr': True,
            'chat': True
        }
    })

@app.route('/config')
def get_config():
    """获取前端配置信息"""
    return jsonify({
        'max_message_length': config.MAX_MESSAGE_LENGTH,
        'voice_name': config.VOICE_NAME,
        'audio_format': config.AUDIO_FORMAT,
        'features': {
            'voice_input': True,
            'voice_output': True
        }
    })

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({'error': '页面不存在'}), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    logger.error(f"服务器内部错误: {str(error)}")
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    # 创建必要目录
    os.makedirs(config.AUDIO_FILES_DIR, exist_ok=True)
    os.makedirs(config.STATIC_DIR, exist_ok=True)
    os.makedirs(config.TEMPLATES_DIR, exist_ok=True)
    
    print("=" * 60)
    print("🎉 黄鹏AI对话工具启动中...")
    print(f"📱 访问地址: http://{config.HOST}:{config.PORT}")
    print("💡 请确保已在config.py中配置API密钥")
    print("🔧 调试模式:", "开启" if config.DEBUG else "关闭")
    print("✨ 新功能: 语音输入 + 语音输出")
    
    # 显示配置验证结果
    if config_validation['warnings']:
        print("⚠️  配置警告:")
        for warning in config_validation['warnings']:
            print(f"   - {warning}")
    
    print("=" * 60)
    
    app.run(
        host=config.HOST, 
        port=config.PORT, 
        debug=config.DEBUG,
        threaded=True
    ) 