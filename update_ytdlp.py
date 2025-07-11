#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yt-dlp 更新脚本
解决 YouTube 字幕获取被封锁的问题
"""

import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_command(cmd):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"✅ 命令执行成功: {cmd}")
            return True, result.stdout
        else:
            logger.error(f"❌ 命令执行失败: {cmd}")
            logger.error(f"错误信息: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        logger.error(f"❌ 命令执行异常: {e}")
        return False, str(e)

def update_ytdlp(channel='nightly'):
    """更新 yt-dlp 到指定版本"""
    
    logger.info(f"🚀 开始更新 yt-dlp 到 {channel} 版本...")
    
    # 检查是否已安装 yt-dlp
    success, output = run_command("yt-dlp --version")
    if success:
        logger.info(f"📍 当前版本: {output.strip()}")
    else:
        logger.info("📍 yt-dlp 未安装，将进行首次安装")
    
    # 更新到指定版本
    if channel == 'stable':
        cmd = "pip install -U yt-dlp"
    elif channel == 'nightly':
        cmd = "pip install -U --pre yt-dlp"
    elif channel == 'master':
        cmd = "pip install -U git+https://github.com/yt-dlp/yt-dlp.git"
    else:
        logger.error(f"❌ 未知版本通道: {channel}")
        return False
    
    logger.info(f"📦 执行安装命令: {cmd}")
    success, output = run_command(cmd)
    
    if success:
        # 验证安装
        success, version = run_command("yt-dlp --version")
        if success:
            logger.info(f"✅ yt-dlp 更新成功！新版本: {version.strip()}")
            
            # 测试 YouTube 连接
            logger.info("🔍 测试 YouTube 连接...")
            test_cmd = 'yt-dlp --list-subs --skip-download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"'
            success, test_output = run_command(test_cmd)
            
            if success:
                logger.info("✅ YouTube 连接测试成功！")
            else:
                logger.warning("⚠️ YouTube 连接测试失败，可能仍需代理")
                
            return True
        else:
            logger.error("❌ 安装验证失败")
            return False
    else:
        logger.error(f"❌ yt-dlp 更新失败: {output}")
        return False

def main():
    """主函数"""
    print("🎬 yt-dlp 更新工具")
    print("=" * 50)
    print("选择更新通道:")
    print("1. stable   - 稳定版 (推荐)")
    print("2. nightly  - 夜间版 (修复最新封锁)")
    print("3. master   - 主分支版 (最新功能)")
    print("=" * 50)
    
    choice = input("请选择 (1-3，默认2): ").strip()
    
    if choice == '1':
        channel = 'stable'
    elif choice == '3':
        channel = 'master'
    else:
        channel = 'nightly'  # 默认选择
    
    print(f"🎯 选择了 {channel} 版本")
    
    success = update_ytdlp(channel)
    
    if success:
        print("\n🎉 更新完成！现在可以重新启动应用测试字幕提取功能。")
        print("💡 如果仍然遇到问题，可以尝试:")
        print("   - 切换到 master 版本")
        print("   - 使用代理服务器")
        print("   - 等待一段时间后重试")
    else:
        print("\n❌ 更新失败！请检查网络连接或手动安装。")
        sys.exit(1)

if __name__ == "__main__":
    main() 