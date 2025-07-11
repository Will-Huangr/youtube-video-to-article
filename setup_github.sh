#!/bin/bash

# 火山引擎视觉API Python SDK - GitHub设置脚本
# 使用方法: ./setup_github.sh [repository_name]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目信息
PROJECT_NAME="volcengine-visual-api"
REPO_NAME=${1:-$PROJECT_NAME}
DESCRIPTION="🚀 火山引擎视觉API Python SDK - 支持图片生成，专为Dify等低代码平台设计"

echo -e "${BLUE}🚀 火山引擎视觉API Python SDK - GitHub设置${NC}"
echo -e "${BLUE}=================================================${NC}"

# 检查是否已经是git仓库
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}📁 初始化Git仓库...${NC}"
    git init
    echo -e "${GREEN}✅ Git仓库初始化完成${NC}"
else
    echo -e "${GREEN}✅ 已存在Git仓库${NC}"
fi

# 添加所有文件
echo -e "${YELLOW}📦 添加项目文件...${NC}"
git add .

# 提交文件
echo -e "${YELLOW}💾 提交初始版本...${NC}"
git commit -m "🎉 Initial release v1.0.0

✨ Features:
- 🔐 Complete AWS V4 signature authentication
- 🎨 Support for VolcEngine Visual API image generation
- 📦 Zero dependencies, Python standard library only
- 🔧 Optimized for Dify code nodes
- 🛡️ Comprehensive error handling
- 📊 Smart parsing of multiple API response formats
- 📝 Detailed documentation and examples

🚀 Ready for production use!"

# 设置默认分支为main
echo -e "${YELLOW}🌿 设置默认分支为main...${NC}"
git branch -M main

echo -e "${BLUE}=================================================${NC}"
echo -e "${GREEN}✅ 本地Git设置完成！${NC}"
echo -e "${BLUE}=================================================${NC}"

echo -e "${YELLOW}📋 接下来的步骤：${NC}"
echo -e "1. 在GitHub上创建新仓库: ${GREEN}https://github.com/new${NC}"
echo -e "2. 仓库名称: ${GREEN}${REPO_NAME}${NC}"
echo -e "3. 描述: ${GREEN}${DESCRIPTION}${NC}"
echo -e "4. 设置为公开仓库"
echo -e "5. 不要初始化README、.gitignore或LICENSE（我们已经有了）"
echo -e "6. 创建仓库后，运行以下命令："
echo -e ""
echo -e "${BLUE}git remote add origin https://github.com/YOUR_USERNAME/${REPO_NAME}.git${NC}"
echo -e "${BLUE}git push -u origin main${NC}"
echo -e ""
echo -e "${YELLOW}💡 提示：${NC}"
echo -e "- 将 YOUR_USERNAME 替换为你的GitHub用户名"
echo -e "- 如果你想要不同的仓库名，重新运行: ${GREEN}./setup_github.sh your-repo-name${NC}"
echo -e ""
echo -e "${GREEN}🎉 准备就绪！${NC}"

# 显示项目结构
echo -e "${BLUE}=================================================${NC}"
echo -e "${YELLOW}📁 项目结构：${NC}"
tree -I '__pycache__|*.pyc|.git' . 2>/dev/null || find . -type f -not -path './.git/*' -not -name '*.pyc' -not -path './__pycache__/*' | sort

echo -e "${BLUE}=================================================${NC}"
echo -e "${GREEN}🚀 项目已准备好发布到GitHub！${NC}" 