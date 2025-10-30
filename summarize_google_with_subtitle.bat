@echo off
chcp 65001 >nul
title YouTube Video Summarizer (Google API - With Subtitle)

REM 切換到腳本所在目錄
cd /d "%~dp0"

echo.
echo ========================================
echo   YouTube Video Summarizer (Google API - With Subtitle)
echo ========================================
echo.

REM Check env var or load from .env
if not defined GOOGLE_API_KEY (
    if exist .env (
        echo Loading API Key from .env...
        for /f "usebackq tokens=1,2 delims==" %%a in (.env) do (
            if "%%a"=="GOOGLE_API_KEY" set GOOGLE_API_KEY=%%b
        )
    )
)

if not defined GOOGLE_API_KEY (
    echo.
    echo ERROR: GOOGLE_API_KEY is not set!
    echo.
    echo Set API Key by either:
    echo 1. Create .env with: GOOGLE_API_KEY=your_api_key
    echo 2. Set system environment variable GOOGLE_API_KEY
    echo.
    echo Get an API Key: https://aistudio.google.com/app/apikey
    echo.
    pause
    exit /b 1
)

set "VIDEO_URL=%~1"

if "%VIDEO_URL%"=="" (
    echo Please input YouTube video URL:
    set /p VIDEO_URL="URL: "
)

if "%VIDEO_URL%"=="" (
    echo.
    echo ERROR: No URL provided!
    pause
    exit /b 1
)

echo.
echo Processing: %VIDEO_URL%
echo Generating summary with Google AI Studio API (with subtitle)...
echo.

REM Check Python availability
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found! Please install Python and add it to PATH.
    echo.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check and install required packages
echo Checking Python packages...
python -c "import google.generativeai, youtube_transcript_api, requests" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing required packages...
    python -m pip install google-generativeai youtube-transcript-api requests
    echo.
) else (
    echo Packages ready. Continue...
)

python youtube_summarizer_google_with_subtitle.py "%VIDEO_URL%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Done! Summary has been saved.
) else (
    echo.
    echo Failed! Please check error messages.
)

echo.
pause
