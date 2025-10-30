#!/usr/bin/env python3
"""YouTube Video Summarizer (Google API 有字幕版本)

This script extracts transcripts from YouTube videos and generates summaries
using Google AI Studio API (Gemini) with minimal dependencies.
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
from typing import Optional

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

# * YouTube 字幕套件檢查
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
MAX_CHUNK_SIZE = 30000
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

def get_video_title(video_id: str) -> str:
    """Get YouTube video title using oEmbed API."""
    try:
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('title', f'Video {video_id}')
    except:
        pass
    return f'Video {video_id}'

def get_transcript(video_id: str, language: str = DEFAULT_LANGUAGE) -> str:
    """Extract transcript from YouTube video."""
    try:
        # * Create API instance
        api = YouTubeTranscriptApi()
        transcript_data = None
        
        # * First, try to list all available transcripts
        try:
            transcript_list = api.list(video_id)
            
            # * Try to get preferred language first (manual or auto)
            for transcript_item in transcript_list:
                if transcript_item.language_code in [language, 'zh', 'en', 'zh-TW', 'zh-CN']:
                    try:
                        transcript_data = transcript_item.fetch()
                        transcript_type = "自動生成" if transcript_item.is_generated else "手動"
                        print(f"✓ 找到 {transcript_item.language_code} 字幕（{transcript_type}）")
                        break
                    except Exception:
                        continue
            
            # * If preferred language not found, get the first available transcript
            if transcript_data is None:
                print("⚠ 未找到偏好語言字幕，嘗試取得其他可用字幕...")
                for transcript_item in transcript_list:
                    try:
                        transcript_data = transcript_item.fetch()
                        transcript_type = "自動生成" if transcript_item.is_generated else "手動"
                        print(f"✓ 找到 {transcript_item.language_code} 字幕（{transcript_type}）")
                        break
                    except Exception:
                        continue
                        
        except TranscriptsDisabled:
            raise TranscriptsDisabled("Transcripts are disabled for this video")
        except Exception:
            # * 繼續嘗試其他方法
            pass
        
        # * If still no transcript found, try direct fetch
        if transcript_data is None:
            try:
                transcript_data = api.fetch(video_id, languages=[language, 'zh', 'en'])
            except Exception:
                pass
        
        # * Check if we have a transcript
        if transcript_data is None:
            raise Exception("無法找到任何可用的字幕")
        
        # * Combine all text segments
        full_text = ' '.join([snippet.text for snippet in transcript_data])
        
        if not full_text.strip():
            raise Exception("字幕內容為空")
        
        print(f"✓ 已取得字幕（共 {len(full_text)} 字元）")
        return full_text
        
    except TranscriptsDisabled:
        raise Exception("此影片已停用字幕功能")
    except VideoUnavailable:
        raise Exception("影片不存在或無法存取")
    except Exception as e:
        error_msg = str(e)
        if "no element found" in error_msg.lower():
            raise Exception("YouTube 字幕服務暫時無法使用，請稍後再試")
        else:
            raise Exception(f"無法取得影片字幕：{error_msg}")

def split_text_into_chunks(text: str, max_size: int = MAX_CHUNK_SIZE) -> list[str]:
    """Split text into chunks for processing."""
    if len(text) <= max_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + max_size
        
        if end < len(text):
            search_start = max(start, end - 200)
            sentence_end = text.rfind('。', search_start, end)
            if sentence_end == -1:
                sentence_end = text.rfind('.', search_start, end)
            if sentence_end == -1:
                sentence_end = text.rfind('！', search_start, end)
            if sentence_end == -1:
                sentence_end = text.rfind('？', search_start, end)
            
            if sentence_end > start:
                end = sentence_end + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end
    
    return chunks

def generate_summary_with_google(text: str, api_key: str) -> str:
    """Generate summary using Google Gemini API."""
    try:
        genai.configure(api_key=api_key)
        # * 使用 Gemini 2.0 Flash（最新且免費的模型）
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
請為以下 YouTube 影片字幕內容生成一個詳細的中文摘要：

{text}

請提供：
1. 影片主要內容概述
2. 關鍵要點（至少 3-5 個）
3. 重要結論或建議

摘要應該：
- 使用繁體中文
- 結構清晰，易於閱讀
- 包含具體的資訊和細節
- 長度適中（約 200-500 字）
"""
        
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text.strip()
        else:
            raise Exception("API 回應為空")
            
    except Exception as e:
        raise Exception(f"Google API 摘要生成失敗：{e}")

def process_video_with_google(video_id: str, api_key: str) -> tuple[str, str]:
    """Process video and generate summary using Google API.
    
    Returns:
        tuple: (summary, video_title)
    """
    print(f"正在處理影片：{video_id}")
    
    title = get_video_title(video_id)
    print(f"影片標題：{title}")
    
    # * 重試機制取得字幕
    max_retries = 3
    transcript = None
    
    for attempt in range(max_retries):
        try:
            print(f"正在取得字幕... (嘗試 {attempt + 1}/{max_retries})")
            transcript = get_transcript(video_id)
            break
        except Exception as e:
            print(f"嘗試 {attempt + 1} 失敗：{e}")
            if attempt < max_retries - 1:
                print("等待 2 秒後重試...")
                import time
                time.sleep(2)
            else:
                raise e
    
    print(f"字幕長度：{len(transcript)} 字元")
    
    chunks = split_text_into_chunks(transcript)
    print(f"分為 {len(chunks)} 個區塊處理")
    
    summaries = []
    for i, chunk in enumerate(chunks):
        print(f"正在處理區塊 {i+1}/{len(chunks)}...")
        try:
            summary = generate_summary_with_google(chunk, api_key)
            summaries.append(f"區塊 {i+1} 摘要：\n{summary}\n")
        except Exception as e:
            print(f"區塊 {i+1} 處理失敗：{e}")
            summaries.append(f"區塊 {i+1}：處理失敗\n")
    
    final_summary = f"影片標題：{title}\n\n" + "\n".join(summaries)
    
    if len(chunks) > 1:
        print("正在生成整體摘要...")
        try:
            overall_summary = generate_summary_with_google(final_summary, api_key)
            final_summary = f"影片標題：{title}\n\n整體摘要：\n{overall_summary}\n\n詳細摘要：\n" + "\n".join(summaries)
        except Exception as e:
            print(f"整體摘要生成失敗：{e}")
    
    return final_summary, title

def save_summary(summary: str, video_id: str, video_title: str = None) -> str:
    """Save summary to file."""
    if video_title:
        # * 使用影片標題命名（與中文最佳版本一致）
        safe_title = sanitize_filename(video_title)
        filename = f"{safe_title}.txt"
    else:
        # * 備用命名方式
        filename = f"summary_{video_id}_google.txt"
    
    try:
        # * 使用 UTF-8 with BOM 確保 Windows 記事本能正確顯示繁體中文
        with open(filename, 'w', encoding='utf-8-sig') as f:
            f.write(f"YouTube 影片摘要 (Google API)\n")
            f.write(f"影片標題：{video_title or f'Video {video_id}'}\n")
            f.write(f"影片 ID：{video_id}\n")
            f.write(f"生成時間：{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"使用模型：Gemini 2.0 Flash\n\n")
            f.write("="*80 + "\n\n")
            f.write(summary)
        return filename
    except Exception as e:
        raise Exception(f"無法儲存摘要檔案：{e}")

def sanitize_filename(title: str) -> str:
    """Sanitize filename by removing invalid characters."""
    # * 移除或替換無效的檔案名字元
    title = re.sub(r'[<>:"/\\|?*]', '_', title)
    # * 移除多餘的空白和特殊字元
    title = re.sub(r'\s+', ' ', title).strip()
    # * 限制長度
    if len(title) > 100:
        title = title[:100]
    return title

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="YouTube 影片摘要生成器 (Google API 有字幕版本)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例：
  python youtube_summarizer_google_with_subtitle.py dQw4w9WgXcQ
  python youtube_summarizer_google_with_subtitle.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  
環境變數：
  GOOGLE_API_KEY - Google AI Studio API Key
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
        
        summary, video_title = process_video_with_google(video_id, api_key)
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
