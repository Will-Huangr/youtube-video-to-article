#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube视频转图文文章生成器 - 修复版本
"""

import os
import json
import logging
from flask import Flask, render_template, request, jsonify
import requests
from youtube_transcript_api import YouTubeTranscriptApi
import re
import subprocess
import tempfile
import glob
import config # 导入配置文件

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)

# API配置
DIFY_API_URL = config.DIFY_API_URL
DIFY_API_KEY = config.DIFY_API_KEY
IMAGE_API_ACCESS_KEY = config.IMAGE_API_ACCESS_KEY
IMAGE_API_SECRET_KEY = config.IMAGE_API_SECRET_KEY

SUPPORTED_LANGUAGES = {
    'en': 'English',
    'zh-Hans': '中文(简体)',
    'zh-Hant': '中文(繁体)',
    'ja': '日本語',
    'ko': '한국어',
    'es': 'Español',
    'fr': 'Français',
    'de': 'Deutsch',
    'ru': 'Русский',
    'ar': 'العربية'
}

def extract_text_from_subtitle(content, file_type='auto'):
    """
    从字幕文件内容中提取纯文本
    支持SRT和VTT格式
    """
    try:
        lines = content.split('\n')
        text_segments = []
        
        if file_type == 'auto':
            # 自动检测格式
            if content.startswith('WEBVTT') or 'WEBVTT' in content[:100]:
                file_type = 'vtt'
            else:
                file_type = 'srt'
        
        if file_type == 'vtt':
            # 处理WebVTT格式
            for line in lines:
                line = line.strip()
                
                # 跳过WebVTT头部、时间戳行、空行、位置信息
                if (not line or 
                    line.startswith('WEBVTT') or 
                    line.startswith('Kind:') or 
                    line.startswith('Language:') or 
                    '-->' in line or
                    'align:start position:' in line or
                    line.startswith('NOTE')):
                    continue
                
                # 去除HTML标签和时间戳标记
                clean_line = re.sub(r'<[^>]+>', '', line)
                clean_line = re.sub(r'<[0-9:.]+>', '', clean_line)
                clean_line = re.sub(r'\s+', ' ', clean_line).strip()
                
                if clean_line:
                    text_segments.append(clean_line)
        
        else:  # SRT格式
            # 处理SRT格式
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                # 跳过空行
                if not line:
                    i += 1
                    continue
                
                # 跳过序号行（纯数字）
                if line.isdigit():
                    i += 1
                    continue
                
                # 跳过时间戳行
                if '-->' in line:
                    i += 1
                    continue
                
                # 处理文本行
                if line and not line.isdigit() and '-->' not in line:
                    # 去除HTML标签
                    clean_line = re.sub(r'<[^>]+>', '', line)
                    clean_line = re.sub(r'\s+', ' ', clean_line).strip()
                    
                    if clean_line:
                        text_segments.append(clean_line)
                
                i += 1
        
        # 合并所有文本
        full_text = ' '.join(text_segments)
        
        # 去重处理 - 移除重复的句子片段
        words = full_text.split()
        unique_words = []
        seen_phrases = set()
        
        # 每5个词作为一个短语进行去重
        for i in range(len(words)):
            word = words[i]
            # 获取当前词及其后面4个词作为短语
            if i + 4 < len(words):
                phrase = ' '.join(words[i:i+5])
                if phrase not in seen_phrases:
                    unique_words.append(word)
                    seen_phrases.add(phrase)
            else:
                unique_words.append(word)
        
        # 重新组合文本
        clean_text = ' '.join(unique_words)
        
        logger.info(f"文本提取完成: 格式={file_type}, 原始长度={len(full_text)}, 去重后长度={len(clean_text)}")
        
        return clean_text
        
    except Exception as e:
        logger.error(f"文本提取失败: {e}")
        raise

def extract_youtube_subtitles_ytdlp(video_url, language='en'):
    """使用yt-dlp提取YouTube字幕的备选方案"""
    try:
        # 提取视频ID
        video_id_match = re.search(r'(?:v=|/)([0-9A-Za-z_-]{11})', video_url)
        if not video_id_match:
            raise Exception("无效的YouTube链接")
        
        video_id = video_id_match.group(1)
        logger.info(f"使用yt-dlp提取视频ID: {video_id}")
        
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 构建yt-dlp命令 - 只下载字幕
            cmd = [
                'yt-dlp',
                '--write-subs',  # 下载字幕
                '--write-auto-subs',  # 下载自动生成的字幕
                '--sub-langs', f'{language},en,en-US',  # 字幕语言优先级
                '--sub-format', 'vtt',  # 字幕格式
                '--skip-download',  # 不下载视频
                '--output', f'{temp_dir}/%(title)s.%(ext)s',
                f'https://www.youtube.com/watch?v={video_id}'
            ]
            
            logger.info("yt-dlp命令: " + ' '.join(cmd))
            
            # 执行命令
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                logger.error(f"yt-dlp执行失败: {result.stderr}")
                raise Exception(f"yt-dlp字幕提取失败: {result.stderr}")
            
            # 查找字幕文件
            subtitle_files = glob.glob(f'{temp_dir}/*.vtt')
            
            if not subtitle_files:
                raise Exception("未找到字幕文件")
            
            # 读取第一个字幕文件
            subtitle_file = subtitle_files[0]
            logger.info(f"找到字幕文件: {subtitle_file}")
            
            with open(subtitle_file, 'r', encoding='utf-8') as f:
                subtitle_content = f.read()
            
            # 使用通用函数提取文本
            clean_text = extract_text_from_subtitle(subtitle_content, 'vtt')
            
            logger.info(f"yt-dlp字幕提取成功，长度: {len(clean_text)} 字符")
            return clean_text
            
    except subprocess.TimeoutExpired:
        logger.error("yt-dlp执行超时")
        raise Exception("yt-dlp执行超时")
    except Exception as e:
        logger.error(f"yt-dlp字幕提取失败: {e}")
        raise

def extract_youtube_subtitles(video_url, language='en'):
    """提取YouTube字幕并本地处理为纯文本 - 带备选方案"""
    try:
        # 首先尝试使用youtube_transcript_api
        logger.info("尝试使用youtube_transcript_api提取字幕...")
        return extract_youtube_subtitles_original(video_url, language)
        
    except Exception as api_error:
        logger.warning(f"youtube_transcript_api失败: {api_error}")
        logger.info("切换到yt-dlp备选方案...")
        
        try:
            return extract_youtube_subtitles_ytdlp(video_url, language)
        except Exception as ytdlp_error:
            logger.error(f"yt-dlp也失败了: {ytdlp_error}")
            raise Exception(f"所有字幕提取方法都失败了。youtube_transcript_api: {str(api_error)[:100]}..., yt-dlp: {str(ytdlp_error)[:100]}...")

def extract_youtube_subtitles_original(video_url, language='en'):
    """提取YouTube字幕并本地处理为纯文本"""
    try:
        # 提取视频ID
        video_id_match = re.search(r'(?:v=|/)([0-9A-Za-z_-]{11})', video_url)
        if not video_id_match:
            raise Exception("无效的YouTube链接")
        
        video_id = video_id_match.group(1)
        logger.info(f"提取视频ID: {video_id}")
        
        # 获取字幕原始数据
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=[language, 'en', 'zh', 'auto'])
        logger.info(f"成功获取字幕，共{len(transcript_data)}条")
        
        # 将transcript_data转换为SRT格式字符串
        srt_content = ""
        for i, entry in enumerate(transcript_data, 1):
            start_time = entry['start']
            duration = entry['duration']
            end_time = start_time + duration
            text = entry['text'].replace('\n', ' ')
            
            def format_srt_time(seconds):
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                secs = int(seconds % 60)
                millis = int((seconds % 1) * 1000)
                return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
            
            start_formatted = format_srt_time(start_time)
            end_formatted = format_srt_time(end_time)
            
            srt_content += f"{i}\n{start_formatted} --> {end_formatted}\n{text}\n\n"
        
        # 使用通用函数提取文本
        clean_text = extract_text_from_subtitle(srt_content, 'srt')
        
        return clean_text
        
    except Exception as e:
        logger.error(f"字幕提取失败: {e}")
        raise

def call_dify_workflow(subtitle_text, language, picture_style):
    """调用Dify工作流"""
    try:
        # 限制文本长度，避免Dify超时
        if len(subtitle_text) > 5000:
            subtitle_text = subtitle_text[:5000]
            logger.info(f"文本过长，截取前5000字符")
        
        dify_url = f"{DIFY_API_URL}/workflows/run"
        headers = {
            'Authorization': f'Bearer {DIFY_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'inputs': {
                'text': subtitle_text,
                'language': language,
                'picturestyle': picture_style or "",
                'secret_key': IMAGE_API_SECRET_KEY,
                'access_key': IMAGE_API_ACCESS_KEY
            },
            'response_mode': 'streaming',  # 使用streaming模式避免超时
            'user': f'user-{hash(subtitle_text) % 100000000}'
        }
        
        logger.info("调用Dify工作流...")
        logger.info(f"字幕长度: {len(subtitle_text)} 字符")
        logger.info(f"参数: language={language}, picturestyle={picture_style}")
        
        # 使用streaming模式，避免CloudFlare 60秒超时
        try:
            logger.info("Dify调用开始（streaming模式），预计需要1-2分钟...")
            
            response = requests.post(dify_url, json=payload, headers=headers, timeout=300, stream=True)
            
            logger.info(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                # 处理streaming响应
                content_parts = []
                title = 'AI生成文章'
                images = []
                final_outputs = {}
                
                for line in response.iter_lines():
                    if line:
                        try:
                            line_str = line.decode('utf-8')
                            if line_str.startswith('data: '):
                                data_str = line_str[6:]  # 去掉 "data: " 前缀
                                if data_str.strip() == '[DONE]':
                                    break
                                
                                data = json.loads(data_str)
                                event = data.get('event', '')
                                
                                if event == 'workflow_finished':
                                    # 工作流完成
                                    outputs = data.get('data', {}).get('outputs', {})
                                    final_outputs = outputs
                                    title = outputs.get('title', 'AI生成文章')
                                    content = outputs.get('content', outputs.get('article', outputs.get('text', '')))
                                    images = outputs.get('images', [])
                                    
                                    # 如果images是字符串，尝试解析
                                    if isinstance(images, str):
                                        try:
                                            images = json.loads(images)
                                        except:
                                            images = []
                                    
                                    logger.info("✅ Dify工作流完成！")
                                    break
                                    
                                elif event == 'node_finished':
                                    # 节点完成
                                    node_data = data.get('data', {})
                                    logger.info(f"节点完成: {node_data.get('title', 'unknown')}")
                                    
                                elif event == 'text_chunk':
                                    # 文本块
                                    chunk = data.get('data', {}).get('text', '')
                                    content_parts.append(chunk)
                                    
                        except json.JSONDecodeError:
                            continue
                        except Exception as e:
                            logger.warning(f"处理streaming数据出错: {e}")
                            continue
                
                # 如果没有从workflow_finished获取到内容，使用累积的内容
                if not final_outputs and content_parts:
                    content = ''.join(content_parts)
                elif final_outputs:
                    content = final_outputs.get('content', final_outputs.get('article', final_outputs.get('text', '')))
                else:
                    content = ''.join(content_parts) if content_parts else '生成失败'
                
                return {
                    'title': title,
                    'content': content,
                    'images': images if isinstance(images, list) else [],
                    'dify_raw': final_outputs
                }
            else:
                logger.error(f"Dify API错误: {response.status_code} - {response.text[:200]}")
                raise Exception(f"Dify API返回错误: {response.status_code}")
                
        except requests.exceptions.Timeout:
            logger.error("Dify调用超时（300秒）")
            raise Exception("Dify API调用超时 - 工作流执行时间过长")
        
    except Exception as e:
        logger.error(f"Dify调用失败: {e}")
        raise

def clean_generated_content(content):
    """清理生成内容中的多余空行和错误信息"""
    if not content:
        return content
    
    # 移除图片相关的错误信息
    lines = content.split('\n')
    cleaned_lines = []
    
    skip_image_error = False
    for line in lines:
        # 检测并跳过图片相关的错误信息
        if '由于提供的图片列表中图片URL为空' in line or '401：未授权' in line:
            skip_image_error = True
            continue
        
        if skip_image_error and ('因此，我将直接输出文章内容' in line or '以下是完整的文章内容' in line):
            skip_image_error = False
            continue
            
        # 跳过连续的空行（超过2个）
        if line.strip() == '':
            # 如果前面已经有空行了，就不再添加
            if cleaned_lines and cleaned_lines[-1].strip() == '':
                continue
        
        cleaned_lines.append(line)
    
    # 移除末尾的连续空行
    while cleaned_lines and cleaned_lines[-1].strip() == '':
        cleaned_lines.pop()
    
    # 移除开头的分隔线
    while cleaned_lines and cleaned_lines[0].strip() in ['---', '']:
        cleaned_lines.pop(0)
    
    return '\n'.join(cleaned_lines).strip()

@app.route('/')
def index():
    """主页"""
    return render_template('index.html', languages=SUPPORTED_LANGUAGES)

@app.route('/api/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'message': 'YouTube视频转图文文章生成器运行正常',
        'config_valid': True
    })

@app.route('/api/process-video', methods=['POST'])
def process_video():
    """处理视频，生成图文文章"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '请提供JSON数据'}), 400
        
        video_url = data.get('video_url', '')
        language = data.get('language', 'en')
        picture_style = data.get('picture_style', '')
        
        if not video_url:
            return jsonify({'error': '请提供视频URL'}), 400
        
        logger.info(f"处理视频: {video_url}")
        
        # 1. 提取字幕
        try:
            subtitle_text = extract_youtube_subtitles(video_url, language)
            logger.info(f"字幕提取成功，长度: {len(subtitle_text)} 字符")
        except Exception as e:
            return jsonify({'error': f'字幕提取失败: {str(e)}'}), 400
        
        # 2. 调用Dify
        try:
            dify_result = call_dify_workflow(subtitle_text, language, picture_style)
            logger.info("Dify调用成功")
            
            # 清理生成的内容
            cleaned_content = clean_generated_content(dify_result['content'])
            
            result = {
                'success': True,
                'message': '视频处理完成 (使用Dify AI生成)',
                'data': {
                    'title': dify_result['title'],
                    'content': cleaned_content,
                    'images': dify_result['images'],
                    'video_info': {
                        'url': video_url,
                        'language': language,
                        'picture_style': picture_style,
                        'duration': '待提取'
                    },
                    'dify_raw': dify_result['dify_raw']
                }
            }
            
            return jsonify(result)
            
        except Exception as e:
            logger.warning(f"Dify调用失败，使用备选方案: {e}")
            
            # 备选方案：基于字幕生成简单文章
            lines = subtitle_text.split('\n')
            text_lines = [line for line in lines if line and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:') and '-->' not in line]
            
            content = ' '.join(text_lines[:50])  # 取前50行字幕
            
            result = {
                'success': True,
                'message': '视频处理完成 (Dify API不可用，使用基础处理)',
                'data': {
                    'title': '基于视频内容的文章',
                    'content': f"# 视频内容摘要\n\n{content}",
                    'images': [
                        {
                            'url': 'https://via.placeholder.com/400x300/667eea/ffffff?text=Video+Content',
                            'description': '视频内容配图',
                            'style': picture_style or 'professional'
                        }
                    ],
                    'video_info': {
                        'url': video_url,
                        'language': language,
                        'picture_style': picture_style,
                        'duration': '待提取'
                    }
                }
            }
            
            return jsonify(result)
        
    except Exception as e:
        logger.error(f"处理失败: {str(e)}")
        return jsonify({'error': f'处理失败: {str(e)}'}), 500

@app.route('/api/demo', methods=['POST'])
def demo_process():
    """Demo接口，直接调用Dify工作流验证流程可行性"""
    try:
        data = request.get_json()
        language = data.get('language', 'en')
        picture_style = data.get('picture_style', 'modern professional style')
        
        logging.info(f"Demo请求 - 语言: {language}, 图片风格: {picture_style}")
        
        # 读取测试文档
        try:
            with open('test_document.txt', 'r', encoding='utf-8') as f:
                test_text = f.read().strip()
        except FileNotFoundError:
            # 如果文件不存在，使用默认文本
            test_text = '''Artificial Intelligence is revolutionizing the way we work and live. Machine learning algorithms can analyze vast amounts of data to identify patterns and make predictions with remarkable accuracy.

Deep learning neural networks mimic the human brain's structure, enabling computers to recognize images, understand natural language, and even generate creative content. Companies across industries are implementing AI solutions to automate processes, improve decision-making, and enhance customer experiences.

The future of AI holds immense potential for breakthroughs in healthcare, education, transportation, and scientific research. As these technologies continue to evolve, they will likely reshape our society in unprecedented ways.

However, the development of AI also raises important questions about ethics, privacy, and the future of human employment. It's crucial that we approach this technological advancement thoughtfully and responsibly.'''
        
        logging.info(f"使用测试文档长度: {len(test_text)} 字符")
        
        # 直接调用Dify工作流
        try:
            logging.info("🚀 开始调用真实Dify工作流...")
            dify_result = call_dify_workflow(test_text, language, picture_style)
            logging.info("✅ Dify工作流调用成功")
            
            # 清理生成的内容
            cleaned_content = clean_generated_content(dify_result['content'])
            
            result = {
                'success': True,
                'message': f'Demo测试成功 - 真实Dify工作流调用',
                'data': {
                    'title': dify_result['title'],
                    'content': cleaned_content,
                    'images': dify_result['images'],
                    'video_info': {
                        'url': 'test_document.txt',
                        'language': language,
                        'picture_style': picture_style,
                        'duration': '测试文档'
                    },
                    'dify_raw': dify_result['dify_raw'],
                    'demo_info': {
                        'input_length': len(test_text),
                        'is_real_dify_call': True
                    }
                }
            }
            
            logging.info(f"Demo成功 - 生成内容长度: {len(cleaned_content)} 字符")
            return jsonify(result)
            
        except Exception as dify_error:
            logging.error(f"Dify调用失败: {str(dify_error)}")
            
            # 如果Dify调用失败，返回错误信息
            result = {
                'success': False,
                'message': f'Demo测试失败 - Dify工作流调用出错',
                'error': str(dify_error),
                'data': {
                    'title': 'Dify调用失败',
                    'content': f'# Dify工作流测试失败\n\n**错误信息**: {str(dify_error)}\n\n**测试文档**: {test_text[:200]}...',
                    'images': [],
                    'demo_info': {
                        'input_length': len(test_text),
                        'is_real_dify_call': True,
                        'error_occurred': True
                    }
                }
            }
            
            return jsonify(result), 500
        
    except Exception as e:
        logging.error(f"Demo处理失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Demo接口处理失败'
        }), 500

if __name__ == '__main__':
    logger.info("🎬 启动YouTube视频转图文文章生成器...")
    logger.info(f"📍 访问地址: http://127.0.0.1:5015")
    
    app.run(
        host='127.0.0.1',
        port=5015,
        debug=True,
        threaded=True
    ) 