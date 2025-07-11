# 🎬 YouTube视频转图文文章生成器

一个基于前端页面和Dify AI的智能内容创作工具，可以将YouTube视频自动转换为图文并茂的文章。

## ✨ 功能特色

- 🎥 **视频内容提取**: 自动下载YouTube视频字幕
- 🤖 **AI智能生成**: 通过Dify工作流生成高质量文章
- 🎨 **智能配图**: 基于文章主题自动生成相关配图
- 📝 **图文结合**: 智能排版，生成图文并茂的最终文章
- 🌐 **简洁界面**: 现代化Web界面，操作简单直观
- ⚡ **一键生成**: 输入视频链接即可完成整个创作流程

## 🎯 应用场景

- **内容创作者**: 快速将视频内容转化为文章
- **自媒体运营**: 批量生成图文内容
- **教育培训**: 将教学视频转换为学习资料
- **企业营销**: 自动化内容生产流程

## 🏗️ 系统架构

```
前端界面 → YouTube字幕提取 → Dify AI处理 → 文章生成 → 配图生成 → 智能排版 → 图文输出
```

## 📱 界面展示

### 主界面
![主界面](screenshots/main-interface.png)
*简洁的视频链接输入界面*

### 处理过程
![处理过程](screenshots/processing.png)
*实时显示处理进度和状态*

### 生成结果展示
![最终结果](screenshots/result.png)
*图文并茂的文章展示，支持预览、编辑和导出*

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/youtube-video-to-article.git
cd youtube-video-to-article

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置说明

#### 2.1 Dify工作流配置
1. 创建新的Dify工作流
2. 配置以下节点：
   - **输入节点**: 接收字幕文本和语言参数
   - **文章生成节点**: 使用大模型生成文章内容
   - **主题提取节点**: 提取文章核心主题
   - **配图生成节点**: 调用图片生成API
   - **输出节点**: 返回完整的图文内容

#### 2.2 环境变量配置
复制配置文件并设置你的API密钥：

```bash
# 复制配置文件模板
cp config.py.example config.py
```

编辑 `config.py` 文件，填入你的配置：

```python
# config.py
DIFY_API_URL = "YOUR_DIFY_WORKFLOW_API_URL"
DIFY_API_KEY = "YOUR_DIFY_API_KEY"

# 图片生成API配置
IMAGE_API_ACCESS_KEY = "YOUR_IMAGE_API_ACCESS_KEY"
IMAGE_API_SECRET_KEY = "YOUR_IMAGE_API_SECRET_KEY"
```

#### 2.3 Dify工作流输入参数
```json
{
  "text": "视频字幕文本内容",
  "language": "语言代码",
  "AccessKeyId": "图片API访问密钥ID",
  "SecretAccessKey": "图片API密钥"
}
```

### 3. 启动应用

```bash
# 启动后端服务
python app.py

# 应用将在默认端口5000启动
# 打开浏览器访问应用界面
```

## 🎯 使用流程

### 1. 启动应用
```bash
# 方式一：直接启动
python app.py

# 方式二：使用自动配置脚本
./setup.sh
```

### 2. 访问界面
- 应用启动后会显示访问地址
- 默认端口：5000
- 在浏览器中打开显示的地址即可使用

### 3. 操作步骤
- **输入视频链接**: 在界面中粘贴YouTube视频链接
- **选择字幕语言**: 从下拉菜单选择合适的语言
- **配置参数**: 根据需要调整文章生成和配图参数
- **开始生成**: 点击生成按钮，系统将自动处理

### 4. 处理流程
- ✅ **视频解析**: 自动获取视频信息和字幕
- 🤖 **AI处理**: 通过Dify工作流生成文章内容
- 🎨 **智能配图**: 基于文章主题生成相关配图
- 📝 **内容整合**: 智能排版生成最终的图文文章

### 5. 获取结果
- **在线预览**: 直接在界面中查看生成的文章
- **内容编辑**: 支持对生成内容进行调整
- **导出功能**: 支持多种格式的内容导出

## 🔧 技术实现

### 前端技术栈
- **HTML5 + CSS3**: 现代化界面设计
- **JavaScript**: 交互逻辑处理
- **响应式设计**: 适配多种设备

### 后端技术栈
- **Python Flask**: Web框架
- **yt-dlp**: YouTube字幕下载
- **Dify API**: AI内容生成
- **图片生成API**: 智能配图生成

### AI处理流程
1. **字幕预处理**: 清理格式，提取纯文本
2. **内容生成**: Dify工作流生成文章
3. **主题提取**: AI理解文章核心内容
4. **配图生成**: 基于主题调用API生成图片
5. **智能排版**: 自动组合图文内容

## 📊 功能特点

| 功能 | 说明 | 优势 |
|------|------|------|
| 视频解析 | 支持YouTube等主流平台 | 兼容性强 |
| 多语言支持 | 支持10+种语言字幕 | 覆盖面广 |
| AI生成 | 基于大模型的内容创作 | 质量高 |
| 智能配图 | API自动生成相关图片 | 视觉效果好 |
| 一键操作 | 简单的用户交互 | 易于使用 |

## 🌐 支持的平台和语言

### 视频平台
- YouTube
- 其他支持字幕的视频平台

### 语言支持
- 中文（简体/繁体）
- English
- 日本語
- 한국어
- Español
- Français
- Deutsch

## 🔧 高级配置

### 环境变量配置
```bash
# 设置Dify相关环境变量
export DIFY_API_URL="YOUR_DIFY_API_URL"
export DIFY_API_KEY="YOUR_DIFY_API_KEY"

# 图片生成API配置
export IMAGE_API_ACCESS_KEY="YOUR_ACCESS_KEY"
export IMAGE_API_SECRET_KEY="YOUR_SECRET_KEY"
```

### Dify工作流配置要点
- **输入参数**: 确保包含 `text`、`language`、`AccessKeyId`、`SecretAccessKey`
- **输出参数**: 包含生成的文章内容和图片URL
- **配图节点**: 在Dify中调用图片生成API
- **模型配置**: 配置合适的大模型和参数
  

### 图片生成API集成
- 支持多种图片生成服务
- 高质量图片生成
- 智能匹配文章主题
- 自动处理API调用和错误

## 🚀 部署说明

### 本地开发
```bash
# 开发环境启动
python app.py
```

### 生产部署
```bash
# 使用Gunicorn部署
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:${PORT:-5000} app:app
```

### Docker部署
```bash
# 构建镜像
docker build -t youtube-to-article .

# 运行容器 (可通过环境变量自定义端口)
docker run -p ${PORT:-5000}:${PORT:-5000} \
  -e DIFY_API_URL="YOUR_API_URL" \
  -e PORT=${PORT:-5000} \
  youtube-to-article
```

### 配置文件模板
创建 `config.py.example` 作为配置模板：

```python
# config.py.example - 配置文件模板
# 复制此文件为 config.py 并填入你的配置

# Dify API 配置
DIFY_API_URL = "YOUR_DIFY_WORKFLOW_API_URL"
DIFY_API_KEY = "YOUR_DIFY_API_KEY"

# 图片生成API配置
IMAGE_API_ACCESS_KEY = "YOUR_IMAGE_API_ACCESS_KEY"
IMAGE_API_SECRET_KEY = "YOUR_IMAGE_API_SECRET_KEY"

# 应用配置
APP_HOST = "0.0.0.0"
APP_PORT = 5000  # 可通过环境变量 PORT 覆盖
DEBUG = False  # 生产环境设为 False
```

## 📈 性能指标

- **处理速度**: 平均2-3分钟完成一篇文章
- **文章质量**: 基于大模型生成，质量稳定
- **配图匹配度**: AI智能匹配，相关性高
- **用户体验**: 简单易用，一键操作

## 🛠️ 开发计划

### 近期计划
- [ ] 支持更多视频平台
- [ ] 增加文章模板选择
- [ ] 优化配图生成算法
- [ ] 添加批量处理功能

### 长期计划
- [ ] 移动端适配
- [ ] 多语言界面
- [ ] 用户系统
- [ ] 内容管理功能

## 🔒 安全说明

- **API密钥安全**: 请勿将API密钥提交到版本控制系统
- **配置文件**: `config.py` 已添加到 `.gitignore`，请使用 `config.py.example` 作为模板
- **环境变量**: 生产环境建议使用环境变量管理敏感配置

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 发起Pull Request

## 📞 联系方式

- 项目地址: [GitHub Repository](https://github.com/YOUR_USERNAME/youtube-video-to-article)
- 问题反馈: [Issues](https://github.com/YOUR_USERNAME/youtube-video-to-article/issues)

## 🙏 致谢

感谢以下开源项目：
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube视频下载工具
- [Flask](https://flask.palletsprojects.com/) - Web框架
- [Dify](https://dify.ai/) - AI工作流平台

---

⭐ 如果这个项目对你有帮助，请给个Star支持一下！ 
