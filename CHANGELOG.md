# 更新日志

## [v1.2.0] - 2024-07-11

### 🎯 主要改进
- **内容智能清理**: 新增 `clean_generated_content()` 函数自动清理AI生成内容中的多余空行和错误信息
- **格式切换修复**: 完全重写格式切换逻辑，修复按钮异常和数据存储问题
- **Markdown渲染优化**: 增强 Markdown 语法支持，支持标题、粗体、斜体、列表、链接等完整语法

### 🛠️ 技术优化
- **数据缓存机制**: 添加全局数据存储，格式切换无需重新处理内容
- **HTML转换改进**: 优化HTML到Markdown的转换算法，支持更多HTML元素
- **前端交互优化**: 改进按钮状态管理和错误处理

### 🐛 Bug修复
- 修复格式切换时按钮状态异常
- 解决生成内容中的多余空行问题
- 修复图片相关错误信息显示问题
- 优化内容显示的字符编码处理

### 📝 文档更新
- 重写 README.md，添加详细使用说明
- 完善项目结构说明
- 添加故障排除指南

## [v1.1.0] - 2024-07-11

### 🚀 新功能
- **yt-dlp集成**: 添加yt-dlp作为YouTube字幕提取的备选方案
- **测试模式**: 新增Demo测试功能，支持绕过YouTube限制
- **多格式支持**: 支持富文本、HTML、Markdown、纯文本四种格式输出
- **格式切换**: 实现一键切换不同格式预览

### 🔧 技术改进
- **双重保障**: youtube_transcript_api + yt-dlp 双重字幕提取机制
- **错误处理**: 改进错误处理和日志记录
- **API健康检查**: 添加完整的API状态监控

### 📋 文档
- 添加 README_YTDLP.md，详细说明yt-dlp使用方法
- 创建 update_ytdlp.py 脚本，便于更新yt-dlp

## [v1.0.0] - 2024-07-11

### 🎉 初始发布
- **基础功能**: YouTube视频字幕提取和AI文章生成
- **Dify集成**: 集成Dify工作流API
- **响应式设计**: 现代化的Web界面
- **多语言支持**: 支持多种语言的字幕提取

### 🔨 技术栈
- **后端**: Flask + Python
- **前端**: 原生JavaScript + CSS3
- **AI**: Dify工作流
- **字幕提取**: YouTube Transcript API

### 📦 功能特性
- YouTube视频链接解析
- 多语言字幕提取
- AI智能文章生成
- 智能配图建议
- 富文本内容展示

---

## 🔗 相关链接

- [项目仓库](https://github.com/your-username/volcengine-visual-api)
- [Dify官网](https://dify.ai/)
- [yt-dlp项目](https://github.com/yt-dlp/yt-dlp)
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api) 