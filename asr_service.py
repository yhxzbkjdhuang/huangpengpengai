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

logger = logging.getLogger(__name__)

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class ASRService:
    def __init__(self, appid, api_key, api_secret):
        self.appid = appid
        self.api_key = api_key
        self.api_secret = api_secret
        self.recognition_result = ""
        self.recognition_complete = False
        self.recognition_error = None
        
    def create_url(self):
        """生成websocket连接URL"""
        url = 'wss://iat-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        
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
            
            logger.info(f"ASR Status Code: {code}")
            
            if code != 0:
                errMsg = message["message"]
                logger.error(f"ASR Error: {errMsg}, Code: {code}")
                self.recognition_error = errMsg
                ws.close()
                return
            
            # 处理识别结果
            data = message.get("data")
            if data:
                result = data.get("result")
                if result:
                    ws_list = result.get("ws")
                    if ws_list:
                        for ws_item in ws_list:
                            cw_list = ws_item.get("cw")
                            if cw_list:
                                for cw_item in cw_list:
                                    self.recognition_result += cw_item.get("w", "")
                
                # 检查是否识别完成
                if data.get("status") == 2:
                    logger.info("ASR recognition complete")
                    self.recognition_complete = True
                    ws.close()
                    
        except Exception as e:
            logger.error(f"处理ASR消息失败: {str(e)}")
            self.recognition_error = str(e)

    def on_error(self, ws, error):
        """处理websocket错误"""
        logger.error(f"ASR WebSocket错误: {error}")
        self.recognition_error = str(error)

    def on_close(self, ws, close_status_code, close_msg):
        """处理websocket关闭"""
        logger.info("ASR WebSocket连接已关闭")

    def on_open(self, ws):
        """处理websocket连接打开"""
        def run(*args):
            # 公共参数
            common_args = {"app_id": self.appid}
            
            # 业务参数
            business_args = {
                "domain": "iat",
                "language": "zh_cn",
                "accent": "mandarin",
                "vinfo": 1,
                "vad_eos": 10000
            }
            
            d = {
                "common": common_args,
                "business": business_args,
                "data": {
                    "status": 0,
                    "format": "audio/L16;rate=16000",
                    "encoding": "raw",
                    "audio": ""
                }
            }
            
            data = json.dumps(d)
            logger.info("发送ASR初始化数据")
            ws.send(data)

        thread.start_new_thread(run, ())

    def send_audio_data(self, ws, audio_data, status):
        """发送音频数据"""
        data = {
            "data": {
                "status": status,
                "format": "audio/L16;rate=16000",
                "encoding": "raw",
                "audio": str(base64.b64encode(audio_data), 'utf-8')
            }
        }
        
        data_json = json.dumps(data)
        ws.send(data_json)

    def recognize(self, audio_data):
        """语音识别主方法"""
        try:
            # 重置状态
            self.recognition_result = ""
            self.recognition_complete = False
            self.recognition_error = None
            
            # 创建websocket连接
            ws_url = self.create_url()
            logger.info(f"连接ASR服务: {ws_url}")
            
            # 设置websocket选项
            ws = websocket.WebSocketApp(
                ws_url,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
                on_open=self.on_open
            )
            
            # 存储websocket实例和音频数据
            self.ws = ws
            self.audio_data = audio_data
            
            # 在新线程中启动websocket连接
            def run_websocket():
                ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
            
            import threading
            ws_thread = threading.Thread(target=run_websocket)
            ws_thread.daemon = True
            ws_thread.start()
            
            # 等待连接建立
            time.sleep(0.5)
            
            # 发送音频数据
            if not self.recognition_error:
                self.send_audio_chunks()
            
            # 等待识别完成
            timeout = 15  # 增加超时时间
            start_time = time.time()
            
            while not self.recognition_complete and not self.recognition_error:
                if time.time() - start_time > timeout:
                    logger.error("ASR识别超时")
                    return None
                time.sleep(0.1)
            
            if self.recognition_error:
                logger.error(f"ASR识别失败: {self.recognition_error}")
                return None
            
            return self.recognition_result
            
        except Exception as e:
            logger.error(f"ASR识别异常: {str(e)}")
            return None

    def send_audio_chunks(self):
        """分块发送音频数据"""
        try:
            chunk_size = 1280  # 每次发送的音频数据大小
            audio_len = len(self.audio_data)
            
            for i in range(0, audio_len, chunk_size):
                chunk = self.audio_data[i:i+chunk_size]
                
                # 确定状态
                if i == 0:
                    status = STATUS_FIRST_FRAME
                elif i + chunk_size >= audio_len:
                    status = STATUS_LAST_FRAME
                else:
                    status = STATUS_CONTINUE_FRAME
                
                self.send_audio_data(self.ws, chunk, status)
                time.sleep(0.04)  # 40ms间隔
                
        except Exception as e:
            logger.error(f"发送音频数据失败: {str(e)}")
            self.recognition_error = str(e) 