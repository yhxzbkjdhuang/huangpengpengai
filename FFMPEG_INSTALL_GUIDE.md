# FFmpeg 安装指南

## 简介
FFmpeg是一个强大的音频视频处理工具，用于将浏览器录制的WebM音频格式转换为语音识别服务所需的PCM格式。

## 安装方法

### Windows 系统

#### 方法1：使用官方下载
1. 访问 [FFmpeg官网](https://ffmpeg.org/download.html)
2. 点击 "Windows" 下的 "Windows builds by BtbN"
3. 下载最新版本的 `ffmpeg-master-latest-win64-gpl.zip`
4. 解压到 `C:\ffmpeg` 目录
5. 将 `C:\ffmpeg\bin` 添加到系统环境变量PATH中

#### 方法2：使用包管理器
```bash
# 使用Chocolatey
choco install ffmpeg

# 使用Scoop
scoop install ffmpeg
```

### macOS 系统

#### 使用Homebrew
```bash
brew install ffmpeg
```

#### 使用MacPorts
```bash
sudo port install ffmpeg
```

### Linux 系统

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

#### CentOS/RHEL
```bash
sudo yum install ffmpeg
# 或者使用 dnf
sudo dnf install ffmpeg
```

#### Arch Linux
```bash
sudo pacman -S ffmpeg
```

## 验证安装

安装完成后，打开命令行工具，输入以下命令验证：

```bash
ffmpeg -version
```

如果显示版本信息，说明安装成功。

## 功能说明

### 有FFmpeg的情况
- ✅ 完整的音频格式转换支持
- ✅ 最佳的语音识别效果
- ✅ 支持各种音频格式

### 没有FFmpeg的情况
- ⚠️ 使用原始音频数据
- ⚠️ 可能影响识别准确率
- ⚠️ 部分浏览器可能不兼容

## 常见问题

### Q: 为什么需要FFmpeg？
A: 浏览器录制的音频通常是WebM格式，而语音识别服务需要PCM格式的音频数据。FFmpeg负责这个转换过程。

### Q: 不安装FFmpeg会怎么样？
A: 系统会尝试直接使用原始音频数据，但可能会影响识别准确率，特别是在某些浏览器中。

### Q: 如何检查FFmpeg是否安装成功？
A: 在命令行中输入 `ffmpeg -version`，如果显示版本信息则安装成功。

### Q: 安装后仍然提示FFmpeg不可用？
A: 请确保FFmpeg已添加到系统PATH环境变量中，或者重启应用程序。

## 技术细节

FFmpeg在本项目中的作用：
1. 将WebM音频转换为PCM格式
2. 设置音频采样率为16kHz
3. 转换为单声道音频
4. 输出为16位有符号整数格式

转换命令示例：
```bash
ffmpeg -i input.webm -acodec pcm_s16le -ar 16000 -ac 1 -f s16le output.pcm
```

## 支持

如果在安装过程中遇到问题，请：
1. 检查官方文档
2. 确认系统版本兼容性
3. 检查环境变量配置
4. 重启应用程序

---

*最后更新时间：2024年12月* 