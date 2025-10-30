#!/usr/bin/env python3
"""YouTube Video Summarizer (Google API 無字幕版本)

This script generates summaries from YouTube videos using Google AI Studio API (Gemini)
without requiring transcripts. It uses video metadata, description, and AI analysis.
"""

# 隱藏 Google 庫的警告訊息
import os
import warnings
import logging

# 設置環境變量隱藏 TensorFlow 警告
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['GRPC_VERBOSITY'] = 'ERROR'

# 隱藏所有警告
warnings.filterwarnings('ignore')

# 設置日誌級別
logging.getLogger('google').setLevel(logging.ERROR)
logging.getLogger('googleapiclient').setLevel(logging.ERROR)
logging.getLogger('google.auth').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)

import argparse
import sys
import re
import json
from typing import Optional, Dict, Any

# * 基本套件檢查
try:
    import requests
except ImportError:
    print("錯誤：缺少 requests 套件。請執行：pip install requests")
    sys.exit(1)

# * Google API 套件檢查
try:
    import google.generativeai as genai
except ImportError:
    print("錯誤：缺少 google-generativeai 套件。請執行：pip install google-generativeai")
    sys.exit(1)

# * YouTube 資料擷取套件檢查
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import (
        TranscriptsDisabled,
        VideoUnavailable
    )
except ImportError:
    print("錯誤：缺少 youtube-transcript-api 套件。請執行：pip install youtube-transcript-api")
    sys.exit(1)

# * ============================================================================
# * Configuration Variables
# * ============================================================================
DEFAULT_LANGUAGE = "zh-TW"
GOOGLE_API_KEY_ENV = "GOOGLE_API_KEY"

# * ============================================================================
# * Helper Functions
# * ============================================================================

def get_google_api_key() -> str:
    """Get Google API key from environment variable."""
    api_key = os.environ.get(GOOGLE_API_KEY_ENV)
    if not api_key:
        raise ValueError(f"請設定環境變數 {GOOGLE_API_KEY_ENV} 或執行 setup_ollama_env.bat")
    return api_key

def extract_video_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from various URL formats."""
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url
    
    patterns = [
        r'(?:youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})',
        r'(?:youtu\.be\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/v\/)([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def get_video_metadata(video_id: str) -> Dict[str, Any]:
    """Get comprehensive video metadata using oEmbed API."""
    try:
        # * 使用 oEmbed API 取得基本資訊
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(url, timeout=10)
        
        metadata = {
            'video_id': video_id,
            'title': f'Video {video_id}',
            'author_name': 'Unknown',
            'description': '',
            'duration': 0,
            'view_count': 0,
            'like_count': 0,
            'published_at': '',
            'tags': []
        }
        
        if response.status_code == 200:
            data = response.json()
            metadata.update({
                'title': data.get('title', metadata['title']),
                'author_name': data.get('author_name', metadata['author_name']),
                'description': data.get('description', metadata['description']),
                'thumbnail_url': data.get('thumbnail_url', ''),
                'html': data.get('html', '')
            })
        
        # * 嘗試取得更多詳細資訊（如果可能）
        try:
            # * 這裡可以加入更多 API 調用來取得詳細資訊
            # * 例如使用 YouTube Data API v3（需要 API key）
            pass
        except Exception:
            pass
            
        return metadata
        
    except Exception as e:
        print(f"警告：無法取得完整影片資訊：{e}")
        return {
            'video_id': video_id,
            'title': f'Video {video_id}',
            'author_name': 'Unknown',
            'description': '',
            'duration': 0,
            'view_count': 0,
            'like_count': 0,
            'published_at': '',
            'tags': []
        }

def try_get_transcript(video_id: str, language: str = DEFAULT_LANGUAGE) -> Optional[str]:
    """Try to get transcript if available, but don't fail if not found."""
    try:
        api = YouTubeTranscriptApi()
        transcript_data = None
        
        # * 嘗試取得字幕
        try:
            transcript_list = api.list(video_id)
            
            for transcript_item in transcript_list:
                if transcript_item.language_code in [language, 'zh', 'en', 'zh-TW', 'zh-CN']:
                    try:
                        transcript_data = transcript_item.fetch()
                        transcript_type = "自動生成" if transcript_item.is_generated else "手動"
                        print(f"✓ 找到 {transcript_item.language_code} 字幕（{transcript_type}）")
                        break
                    except Exception:
                        continue
            
            if transcript_data is None:
                for transcript_item in transcript_list:
                    try:
                        transcript_data = transcript_item.fetch()
                        transcript_type = "自動生成" if transcript_item.is_generated else "手動"
                        print(f"✓ 找到 {transcript_item.language_code} 字幕（{transcript_type}）")
                        break
                    except Exception:
                        continue
                        
        except Exception:
            pass
        
        if transcript_data:
            full_text = ' '.join([snippet.text for snippet in transcript_data])
            if full_text.strip():
                print(f"✓ 已取得字幕（共 {len(full_text)} 字元）")
                return full_text
        
        return None
        
    except Exception:
        return None

def generate_summary_with_google(metadata: Dict[str, Any], transcript: Optional[str] = None, api_key: str = None) -> str:
    """Generate summary using Google Gemini API with available information."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # * 構建提示詞
        prompt_parts = [
            "請根據以下 YouTube 影片資訊生成一個詳細的中文摘要：",
            "",
            f"影片標題：{metadata['title']}",
            f"頻道名稱：{metadata['author_name']}",
            f"影片描述：{metadata['description']}",
            f"影片 ID：{metadata['video_id']}",
        ]
        
        if transcript:
            prompt_parts.extend([
                "",
                "影片字幕內容：",
                transcript
            ])
        else:
            prompt_parts.extend([
                "",
                "注意：此影片沒有可用的字幕，請根據標題、描述和頻道資訊進行分析。"
            ])
        
        prompt_parts.extend([
            "",
            "請提供：",
            "1. 影片主要內容概述（基於標題和描述）",
            "2. 預期關鍵要點（至少 3-5 個）",
            "3. 影片類型分析",
            "4. 目標觀眾分析",
            "5. 建議觀看重點",
            "",
            "摘要應該：",
            "- 使用繁體中文",
            "- 結構清晰，易於閱讀",
            "- 基於可用資訊進行合理推測",
            "- 長度適中（約 200-500 字）",
            "- 如果沒有字幕，請明確說明並提供基於標題描述的合理分析"
        ])
        
        prompt = "\n".join(prompt_parts)
        
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text.strip()
        else:
            raise Exception("API 回應為空")
            
    except Exception as e:
        raise Exception(f"Google API 摘要生成失敗：{e}")

def process_video_without_subtitle(video_id: str, api_key: str) -> tuple[str, str]:
    """Process video and generate summary without requiring transcript.
    
    Returns:
        tuple: (summary, video_title)
    """
    print(f"正在處理影片：{video_id}")
    
    # * 取得影片基本資訊
    metadata = get_video_metadata(video_id)
    print(f"影片標題：{metadata['title']}")
    print(f"頻道名稱：{metadata['author_name']}")
    
    # * 嘗試取得字幕（可選）
    transcript = try_get_transcript(video_id)
    
    if transcript:
        print("✓ 找到字幕，將結合字幕和基本資訊生成摘要")
    else:
        print("⚠ 未找到字幕，將基於標題和描述生成摘要")
    
    # * 生成摘要
    print("正在生成摘要...")
    summary = generate_summary_with_google(metadata, transcript, api_key)
    
    return summary, metadata['title']

def save_summary(summary: str, video_id: str, video_title: str = None) -> str:
    """Save summary to file."""
    if video_title:
        safe_title = sanitize_filename(video_title)
        filename = f"{safe_title}_無字幕版.txt"
    else:
        filename = f"summary_{video_id}_google_no_subtitle.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8-sig') as f:
            f.write(f"YouTube 影片摘要 (Google API 無字幕版)\n")
            f.write(f"影片標題：{video_title or f'Video {video_id}'}\n")
            f.write(f"影片 ID：{video_id}\n")
            f.write(f"生成時間：{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"使用模型：Gemini 2.0 Flash\n")
            f.write(f"摘要類型：無字幕分析\n\n")
            f.write("="*80 + "\n\n")
            f.write(summary)
        return filename
    except Exception as e:
        raise Exception(f"無法儲存摘要檔案：{e}")

def sanitize_filename(title: str) -> str:
    """Sanitize filename by removing invalid characters."""
    title = re.sub(r'[<>:"/\\|?*]', '_', title)
    title = re.sub(r'\s+', ' ', title).strip()
    if len(title) > 100:
        title = title[:100]
    return title

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="YouTube 影片摘要生成器 (Google API 無字幕版本)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例：
  python youtube_summarizer_google_no_subtitle.py dQw4w9WgXcQ
  python youtube_summarizer_google_no_subtitle.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  
環境變數：
  GOOGLE_API_KEY - Google AI Studio API Key

注意：
  此版本不需要字幕即可生成摘要，會基於影片標題、描述和基本資訊進行分析。
  如果影片有字幕，會優先使用字幕內容；如果沒有字幕，會基於其他資訊進行合理推測。
        """
    )
    
    parser.add_argument(
        'video_url',
        help='YouTube 影片網址或影片 ID'
    )
    
    parser.add_argument(
        '--language',
        default=DEFAULT_LANGUAGE,
        help=f'字幕語言偏好 (預設: {DEFAULT_LANGUAGE})'
    )
    
    args = parser.parse_args()
    
    try:
        api_key = get_google_api_key()
        
        video_id = extract_video_id(args.video_url)
        if not video_id:
            print("錯誤：無法從網址中提取影片 ID")
            sys.exit(1)
        
        summary, video_title = process_video_without_subtitle(video_id, api_key)
        filename = save_summary(summary, video_id, video_title)
        
        print(f"\n摘要已儲存至：{filename}")
        print("\n摘要內容：")
        print("=" * 50)
        print(summary)
        
    except Exception as e:
        print(f"錯誤：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


