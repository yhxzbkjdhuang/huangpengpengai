# -*- coding:utf-8 -*-
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os
import logging
import tempfile
import wave

logger = logging.getLogger(__name__)

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class TTSService:
    def __init__(self, appid, api_key, api_secret):
        self.appid = appid
        self.api_key = api_key
        self.api_secret = api_secret
        self.audio_data = bytearray()
        self.synthesis_complete = False
        self.synthesis_error = None
        
    def create_url(self):
        """生成websocket连接URL"""
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'), 
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.api_key, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        return url

    def on_message(self, ws, message):
        """处理websocket消息"""
        try:
            message = json.loads(message)
            code = message["code"]
            sid = message["sid"]
            audio = message["data"]["audio"]
            audio = base64.b64decode(audio)
            status = message["data"]["status"]
            
            logger.info(f"TTS Status: {status}, Code: {code}")
            
            if status == 2:
                logger.info("TTS synthesis complete")
                self.synthesis_complete = True
                ws.close()
                
            if code != 0:
                errMsg = message["message"]
                logger.error(f"TTS Error: {errMsg}, Code: {code}")
                self.synthesis_error = errMsg
                ws.close()
            else:
                # 收集音频数据
                self.audio_data.extend(audio)
                
        except Exception as e:
            logger.error(f"处理TTS消息失败: {str(e)}")
            self.synthesis_error = str(e)
            ws.close()

    def on_error(self, ws, error):
        """处理websocket错误"""
        logger.error(f"TTS WebSocket错误: {error}")
        self.synthesis_error = str(error)

    def on_close(self, ws, close_status_code, close_msg):
        """处理websocket关闭"""
        logger.info("TTS WebSocket连接已关闭")

    def on_open(self, ws, text):
        """处理websocket连接打开"""
        def run(*args):
            # 公共参数
            common_args = {"app_id": self.appid}
            
            # 业务参数
            business_args = {
                "aue": "raw", 
                "auf": "audio/L16;rate=16000", 
                "vcn": "aisjiuxu", 
                "tte": "utf8"
            }
            
            # 数据参数
            data_args = {
                "status": 2, 
                "text": str(base64.b64encode(text.encode('utf-8')), "UTF8")
            }
            
            d = {
                "common": common_args,
                "business": business_args,
                "data": data_args,
            }
            
            d = json.dumps(d)
            logger.info("发送TTS请求数据")
            ws.send(d)

        thread.start_new_thread(run, ())

    def synthesize(self, text):
        """语音合成主方法"""
        try:
            # 重置状态
            self.audio_data = bytearray()
            self.synthesis_complete = False
            self.synthesis_error = None
            
            # 创建websocket连接
            ws_url = self.create_url()
            
            # 设置websocket选项
            ws = websocket.WebSocketApp(
                ws_url,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            
            # 设置on_open回调，传递文本
            ws.on_open = lambda ws: self.on_open(ws, text)
            
            # 启动websocket连接
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
            
            # 等待合成完成
            timeout = 30  # 30秒超时
            start_time = time.time()
            
            while not self.synthesis_complete and not self.synthesis_error:
                if time.time() - start_time > timeout:
                    logger.error("TTS合成超时")
                    return None
                time.sleep(0.1)
            
            if self.synthesis_error:
                logger.error(f"TTS合成失败: {self.synthesis_error}")
                return None
            
            # 转换PCM数据为WAV格式
            return self.convert_pcm_to_wav(self.audio_data)
            
        except Exception as e:
            logger.error(f"TTS合成异常: {str(e)}")
            return None

    def convert_pcm_to_wav(self, pcm_data):
        """将PCM数据转换为WAV格式"""
        try:
            # 创建临时文件
            timestamp = int(time.time() * 1000)
            wav_filename = f"audio_{timestamp}.wav"
            wav_path = os.path.join('audio_files', wav_filename)
            
            # 确保目录存在
            os.makedirs('audio_files', exist_ok=True)
            
            # 使用wave模块创建WAV文件
            with wave.open(wav_path, 'wb') as wav_file:
                wav_file.setnchannels(1)  # 单声道
                wav_file.setsampwidth(2)  # 16位
                wav_file.setframerate(16000)  # 16kHz采样率
                wav_file.writeframes(pcm_data)
            
            logger.info(f"成功生成WAV文件: {wav_path}")
            return wav_path
            
        except Exception as e:
            logger.error(f"PCM转WAV失败: {str(e)}")
            return None 