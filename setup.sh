#!/bin/bash

# YouTube视频转图文文章生成器 - 环境设置脚本
# YouTube Video to Article Generator - Environment Setup Script

echo "🎬 YouTube视频转图文文章生成器 - 环境设置"
echo "=========================================="
echo ""

# 检查Python版本
echo "📋 检查Python环境..."
python_version=$(python3 --version 2>/dev/null || python --version 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ Python已安装: $python_version"
else
    echo "❌ 未找到Python，请先安装Python 3.8+"
    exit 1
fi

# 创建虚拟环境
echo ""
echo "🔧 创建Python虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv 2>/dev/null || python -m venv venv
    echo "✅ 虚拟环境创建成功"
else
    echo "✅ 虚拟环境已存在"
fi

# 激活虚拟环境
echo ""
echo "🚀 激活虚拟环境..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate
echo "✅ 虚拟环境已激活"

# 安装依赖
echo ""
echo "📦 安装项目依赖..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ 依赖安装完成"
else
    echo "⚠️  requirements.txt 文件不存在，手动安装基础依赖..."
    pip install flask youtube-transcript-api requests
fi

# 配置文件设置
echo ""
echo "⚙️  配置项目..."
if [ ! -f "config.py" ]; then
    if [ -f "config.py.example" ]; then
        cp config.py.example config.py
        echo "✅ 配置文件已创建: config.py"
        echo ""
        echo "🔑 请编辑 config.py 文件，填入你的API配置:"
        echo "   - DIFY_API_URL: 你的Dify工作流API地址"
        echo "   - DIFY_API_KEY: 你的Dify API密钥"
        echo "   - IMAGE_API_ACCESS_KEY: 图片生成API访问密钥"
        echo "   - IMAGE_API_SECRET_KEY: 图片生成API密钥"
    else
        echo "❌ config.py.example 文件不存在"
    fi
else
    echo "✅ 配置文件已存在: config.py"
fi

# 创建必要目录
echo ""
echo "📁 创建项目目录..."
mkdir -p screenshots
mkdir -p temp
mkdir -p logs
echo "✅ 目录创建完成"

# 启动提示
echo ""
echo "🎉 环境设置完成！"
echo ""
echo "📝 下一步操作:"
echo "1. 编辑 config.py 文件，填入你的API配置"
echo "2. 运行应用: python run.py"
echo "3. 浏览器访问应用: http://127.0.0.1:8080"
echo ""
echo "📚 更多信息请查看 README.md 文件"
echo ""
echo "🧪 如果遇到YouTube IP限制，可以使用Demo测试功能"

echo ""
echo "🚀 准备就绪! 运行 'python run.py' 启动应用" 