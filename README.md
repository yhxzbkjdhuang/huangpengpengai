# 🎉 黄鹏AI对话工具

> 专为"谢猪猪"定制的AI对话系统 💝

![系统状态](https://img.shields.io/badge/状态-正常运行-brightgreen)
![测试状态](https://img.shields.io/badge/测试-6/6通过-success)
![Python版本](https://img.shields.io/badge/Python-3.7+-blue)
![许可证](https://img.shields.io/badge/许可证-MIT-green)

## 🌟 项目简介

黄鹏AI对话工具是一个集成了语音输入、语音输出和智能对话的现代化AI助手系统。黄鹏是一个风趣幽默的AI角色，专门为"谢猪猪"定制，提供贴心、有趣的对话体验。

### ✨ 核心特性

- 🤖 **个性化AI角色** - 黄鹏，风趣幽默的专属AI小伙伴
- 💬 **智能对话** - 基于Kimi API的自然语言对话，支持上下文记忆
- 🎤 **语音输入** - 科大讯飞ASR语音识别，点击或按空格键录音
- 🔊 **语音输出** - 科大讯飞TTS语音合成，可播放AI回复
- 📱 **现代化UI** - 响应式设计，支持移动端和桌面端
- 🚀 **实时反馈** - 状态提示、加载动画、错误处理
- 🎯 **专属定制** - 总是称呼用户为"谢猪猪"，贴心关怀

## 🚀 快速开始

### 方法1：一键启动（推荐）
```bash
# Windows用户
双击 quick_start.bat

# 或者命令行
python start.py
```

### 方法2：手动启动
```bash
# 1. 克隆项目
git clone <repository-url>
cd ai2

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置API密钥（见配置说明）
# 编辑 config.py 文件

# 4. 启动应用
python app.py
```

### 访问应用
- 本地访问：http://127.0.0.1:5000
- 局域网访问：http://192.168.1.150:5000

## ⚙️ 配置说明

### 1. API密钥配置

在 `config.py` 中配置以下API密钥：

```python
# Kimi API配置（对话功能）
KIMI_API_KEY = "your_kimi_api_key_here"

# 科大讯飞配置（语音功能）
XFYUN_APPID = "your_xfyun_appid_here"
XFYUN_API_KEY = "your_xfyun_api_key_here"
XFYUN_API_SECRET = "your_xfyun_api_secret_here"
```

### 2. 获取API密钥

#### Kimi API
1. 访问 [月之暗面开放平台](https://platform.moonshot.cn/)
2. 注册账号并创建应用
3. 获取API密钥

#### 科大讯飞API
1. 访问 [科大讯飞开放平台](https://www.xfyun.cn/)
2. 注册账号并创建应用
3. 开通"语音听写"和"语音合成"服务
4. 获取APPID、API Key和API Secret

### 3. 环境变量配置（可选）

```bash
# 设置环境变量
export KIMI_API_KEY="your_kimi_api_key"
export XFYUN_APPID="your_xfyun_appid"
export XFYUN_API_KEY="your_xfyun_api_key"
export XFYUN_API_SECRET="your_xfyun_api_secret"
```

## 🛠️ 技术架构

### 后端技术栈
- **Flask** - Web框架
- **Kimi API** - 对话AI服务
- **科大讯飞TTS** - 语音合成
- **科大讯飞ASR** - 语音识别
- **WebSocket** - 实时通信
- **FFmpeg** - 音频处理（可选）

### 前端技术栈
- **HTML5** - 结构标记
- **CSS3** - 样式设计
- **JavaScript** - 交互逻辑
- **Bootstrap 5** - UI组件
- **Web Audio API** - 音频处理

## 📁 项目结构

```
ai2/
├── app.py                    # Flask主应用
├── config.py                 # 配置管理
├── tts_service.py           # 语音合成服务
├── asr_service.py           # 语音识别服务
├── start.py                 # 启动脚本
├── test_system.py           # 系统测试脚本
├── quick_start.bat          # Windows快速启动
├── requirements.txt         # 依赖包列表
├── templates/
│   └── index.html          # 前端页面
├── static/
│   ├── css/
│   │   └── style.css       # 样式文件
│   └── js/
│       └── chat.js         # 前端逻辑
├── audio_files/            # 音频文件目录
├── README.md               # 项目说明
├── FINAL_GUIDE.md          # 完整使用指南
├── VOICE_INPUT_GUIDE.md    # 语音输入指南
├── FFMPEG_INSTALL_GUIDE.md # FFmpeg安装指南
└── TROUBLESHOOTING.md      # 故障排除指南
```

## 🎯 功能详解

### 💬 智能对话
- **个性化角色**：黄鹏，风趣幽默的AI小伙伴
- **专属称呼**：总是称呼用户为"谢猪猪"
- **对话风格**：轻松幽默，贴心关怀
- **上下文记忆**：支持多轮对话，保持话题连贯性
- **快速回复**：预设常用问题，一键发送

### 🎤 语音输入
- **录音方式**：点击麦克风按钮或按空格键
- **实时反馈**：录音状态、识别进度显示
- **自动发送**：识别成功后自动发送消息
- **错误处理**：权限、网络等问题的友好提示
- **音频格式**：支持WebM到PCM格式转换

### 🔊 语音输出
- **语音合成**：科大讯飞TTS，自然流畅
- **发音人选择**：默认x4_yezi，可自定义
- **播放控制**：点击播放按钮播放AI回复
- **状态反馈**：加载、播放、错误状态提示
- **资源管理**：自动清理临时音频文件

### 📱 用户界面
- **响应式设计**：适配手机、平板、电脑
- **现代化风格**：渐变背景、圆角设计、动画效果
- **状态指示**：在线状态、字符计数、语音状态
- **交互反馈**：按钮动画、消息动画、加载提示

## 🧪 测试验证

### 运行系统测试
```bash
python test_system.py
```

### 测试项目
- ✅ 文件结构检查
- ✅ 配置验证
- ✅ 服务器状态
- ✅ 系统组件
- ✅ 对话功能
- ✅ 语音合成

### 手动测试
```bash
# 检查服务状态
curl http://localhost:5000/health

# 查看组件状态
curl http://localhost:5000/test

# 测试对话API
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好", "history": []}'
```

## 🔧 依赖包

### 核心依赖
```
Flask==2.3.3
Flask-CORS==4.0.0
requests==2.31.0
websocket-client==1.6.4
```

### 完整依赖列表
查看 `requirements.txt` 文件获取完整的依赖包列表。

## 🚨 常见问题

### 语音功能问题
- **麦克风权限**：确保浏览器允许麦克风访问
- **网络连接**：检查与语音服务的连接
- **音频质量**：在安静环境中录音
- **FFmpeg安装**：参考 `FFMPEG_INSTALL_GUIDE.md`

### 配置问题
- **API密钥**：确保密钥正确且有效
- **网络访问**：检查防火墙和代理设置
- **端口占用**：默认5000端口，可在config.py中修改

### 性能优化
- **安装FFmpeg**：获得更好的音频处理效果
- **网络优化**：使用稳定的网络连接
- **资源管理**：定期清理临时文件

## 📚 文档索引

- [FINAL_GUIDE.md](FINAL_GUIDE.md) - 完整使用指南
- [VOICE_INPUT_GUIDE.md](VOICE_INPUT_GUIDE.md) - 语音输入详细指南
- [FFMPEG_INSTALL_GUIDE.md](FFMPEG_INSTALL_GUIDE.md) - FFmpeg安装指南
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 故障排除指南

## 🔐 安全建议

### 生产环境
1. **修改SECRET_KEY**：在config.py中设置安全的密钥
2. **关闭DEBUG模式**：设置 `DEBUG = False`
3. **使用HTTPS**：配置SSL证书
4. **限制访问**：设置防火墙规则
5. **监控日志**：定期检查应用日志

### API密钥管理
- 使用环境变量存储敏感信息
- 定期轮换API密钥
- 监控API使用量和费用

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境设置
```bash
# 1. Fork项目
# 2. 克隆到本地
git clone <your-fork-url>
cd ai2

# 3. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 运行测试
python test_system.py
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 💝 特别致谢

这个系统专为"谢猪猪"定制，希望黄鹏AI能成为您的贴心小伙伴！

### 系统特色
- 🎭 **个性化角色**：黄鹏的独特性格设定
- 💕 **专属称呼**：总是亲切地称呼"谢猪猪"
- 🌟 **贴心服务**：关心用户情感，提供温暖陪伴
- 🎉 **趣味互动**：幽默风趣，让对话更有乐趣

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 📧 Email: [yhxzbkjd@outlook.com]
- 🐛 Issues: [GitHub Issues]
- 💬 讨论: [GitHub Discussions]

---

**🎉 享受与黄鹏AI的愉快对话吧！** 💬✨

*最后更新时间：2025年07月* 