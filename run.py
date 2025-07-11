#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的应用启动脚本
"""

if __name__ == '__main__':
    try:
        # 导入本地配置
        import config_local
    except ImportError:
        pass
    
    from app import app
    
    print("🚀 启动YouTube视频转图文文章生成器...")
    print("📍 访问地址: http://127.0.0.1:8080")
    
    app.run(
        host='127.0.0.1',
        port=8080,
        debug=True
    ) 