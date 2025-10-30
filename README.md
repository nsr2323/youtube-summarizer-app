# YouTube Video Summarizer

An automated YouTube video summarization tool using Google AI Studio API (Gemini).

## Features

### With Subtitle Version (`youtube_summarizer_google_with_subtitle.py`)
- ✅ Automatic YouTube video transcript extraction
- ✅ Multi-language subtitle support (prioritizes Traditional Chinese, Chinese, English)
- ✅ Intelligent chunking for long videos
- ✅ High-quality summaries using Google Gemini 2.0 Flash model
- ✅ Automatic retry mechanism for stability

### No Subtitle Version (`youtube_summarizer_google_no_subtitle.py`)
- ✅ Generate summaries without requiring subtitles
- ✅ Analysis based on video title, description, and metadata
- ✅ Prioritizes subtitle content if available
- ✅ Perfect for videos without subtitles

## Installation

### 1. Install Python
Ensure Python 3.7 or higher is installed:
- Download: https://www.python.org/downloads/
- Check "Add Python to PATH" during installation

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install google-generativeai youtube-transcript-api requests
```

### 3. Get Google AI Studio API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key" to generate a new API key
4. Copy the generated API key

### 4. Configure API Key
Choose one of the following methods:

#### Method 1: Using .env file (Recommended)
1. Copy `env.example` to `.env`
2. Edit `.env` file and replace `your_google_api_key_here` with your actual API key:
```
GOOGLE_API_KEY=your_actual_api_key
```

#### Method 2: Set system environment variable
**Windows:**
```cmd
setx GOOGLE_API_KEY "your_actual_api_key"
```

**macOS/Linux:**
```bash
export GOOGLE_API_KEY="your_actual_api_key"
```

## Usage

### Command Line

#### With Subtitle Version
```bash
python youtube_summarizer_google_with_subtitle.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### No Subtitle Version
```bash
python youtube_summarizer_google_no_subtitle.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### How to convert commands into a .bat file
- Method 1: Save as a new file
  1. Open Notepad
  2. Paste the batch content (see templates in this repo)
  3. Save As:
     - File name: e.g., `summarize_google_with_subtitle.bat`
     - Save as type: "All Files (*.*)"
     - Encoding: Prefer "ANSI" or "UTF-8 without BOM". Using UTF-8 with BOM may introduce strange characters in the first line.
- Method 2: Copy from a template
  - Copy an existing `.bat`, rename it, and edit as needed
- Encoding and code page notes
  - We use `chcp 65001 >nul` at the top for proper UTF-8 output
  - If you see garbled text, re-save as ANSI or UTF-8 without BOM
- Common issues
  - Double-click does nothing: ensure the extension is `.bat` (not `.txt`)
  - Python not found: install Python and add it to PATH
  - API key not loaded: ensure `.env` sits next to the `.bat` and contains `GOOGLE_API_KEY=your_key`
- Security note
  - Do not hardcode your API key in `.bat`. Use `.env` or system environment variables

Minimal wrapper example:
```bat
@echo off
chcp 65001 >nul
cd /d "%~dp0"
if not defined GOOGLE_API_KEY (
  if exist .env (
    for /f "usebackq tokens=1,2 delims==" %%a in (.env) do (
      if "%%a"=="GOOGLE_API_KEY" set GOOGLE_API_KEY=%%b
    )
  )
)
if not defined GOOGLE_API_KEY (
  echo GOOGLE_API_KEY is not set. Create .env or set a system env var.
  pause & exit /b 1
)
set "VIDEO_URL=%~1"
if "%VIDEO_URL%"=="" (
  set /p VIDEO_URL=Enter YouTube URL:
)
python youtube_summarizer_google_with_subtitle.py "%VIDEO_URL%"
pause
```

### Batch File Usage (Windows)

#### With Subtitle Version
1. Double-click `summarize_google_with_subtitle.bat`
2. Enter YouTube video URL
3. Wait for processing to complete

#### No Subtitle Version
1. Double-click `summarize_google_no_subtitle.bat`
2. Enter YouTube video URL
3. Wait for processing to complete

### Parameters
- `--language`: Specify subtitle language preference (default: zh-TW)
- Supported URL formats:
  - `https://www.youtube.com/watch?v=VIDEO_ID`
  - `https://youtu.be/VIDEO_ID`
  - `VIDEO_ID` (direct video ID input)

## Output Files

Summaries are saved as text files with naming format:
- With subtitle version: `Video_Title.txt`
- No subtitle version: `Video_Title_no_subtitle.txt`

Files contain:
- Video metadata
- Generation timestamp
- AI model used
- Detailed summary content

## FAQ

### Q: Getting "No available transcript found" error
**A:** The video likely has no subtitles. Use the no-subtitle version:
```bash
python youtube_summarizer_google_no_subtitle.py "video_url"
```

### Q: Getting "Please set environment variable GOOGLE_API_KEY" error
**A:** Follow the API key setup steps above. Ensure:
1. `.env` file exists and is formatted correctly
2. Or system environment variable is properly set
3. API key is valid and not expired

### Q: Processing fails or poor summary quality
**A:** Possible causes:
1. Network connection issues
2. API key quota exceeded
3. Video content too complex
4. Try re-running or use a different video

### Q: What subtitle languages are supported?
**A:** Priority order: zh-TW (Traditional Chinese) > zh-CN (Simplified Chinese) > en (English) > others available

## Technical Specifications

- **Python Version**: 3.7+
- **AI Model**: Google Gemini 2.0 Flash
- **Max Processing Length**: 30,000 characters/chunk
- **Supported Formats**: YouTube standard URL formats
- **Output Format**: UTF-8 text files

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## Contributing

Issues and Pull Requests are welcome!

## Changelog

- v1.0.0: Initial release with both subtitle and no-subtitle modes
