# YouTube 影片摘要生成器

一個使用 Google AI Studio API (Gemini) 自動生成 YouTube 影片摘要的 Python 工具。

## 功能特色

### 有字幕版本 (`youtube_summarizer_google_with_subtitle.py`)
- ✅ 自動提取 YouTube 影片字幕
- ✅ 支援多語言字幕（優先繁體中文、中文、英文）
- ✅ 智能分塊處理長影片
- ✅ 使用 Google Gemini 2.0 Flash 模型生成高品質摘要
- ✅ 自動重試機制確保穩定性

### 無字幕版本 (`youtube_summarizer_google_no_subtitle.py`)
- ✅ 無需字幕即可生成摘要
- ✅ 基於影片標題、描述和基本資訊進行分析
- ✅ 如果影片有字幕，會優先使用字幕內容
- ✅ 適合處理沒有字幕的影片

## 安裝步驟

### 1. 安裝 Python
確保您的系統已安裝 Python 3.7 或更高版本：
- 下載：https://www.python.org/downloads/
- 安裝時請勾選 "Add Python to PATH"

### 2. 安裝依賴套件
```bash
pip install -r requirements.txt
```

或手動安裝：
```bash
pip install google-generativeai youtube-transcript-api requests
```

### 3. 申請 Google AI Studio API Key
1. 前往 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 登入您的 Google 帳號
3. 點擊 "Create API Key" 建立新的 API Key
4. 複製生成的 API Key

### 4. 設定 API Key
選擇以下方式之一設定 API Key：

#### 方式一：使用 .env 檔案（推薦）
1. 複製 `env.example` 為 `.env`
2. 編輯 `.env` 檔案，將 `your_google_api_key_here` 替換為您的實際 API Key：
```
GOOGLE_API_KEY=您的實際API金鑰
```

#### 方式二：設定系統環境變數
**Windows:**
```cmd
setx GOOGLE_API_KEY "您的實際API金鑰"
```

**macOS/Linux:**
```bash
export GOOGLE_API_KEY="您的實際API金鑰"
```

## 使用說明

### 命令列使用

#### 有字幕版本
```bash
python youtube_summarizer_google_with_subtitle.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### 無字幕版本
```bash
python youtube_summarizer_google_no_subtitle.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### 如何把命令轉成 .bat 批次檔
- 方法一：另存新檔
  1. 開啟記事本（Notepad）
  2. 貼上批次內容（可參考本專案的 `.bat` 範本）
  3. 另存新檔：
     - 檔名：例如 `summarize_google_with_subtitle.bat`
     - 儲存類型：選「所有檔案（*.*）」
     - 編碼：建議「ANSI」或「UTF-8（無 BOM）」；若使用 UTF-8（有 BOM），可能在第一行出現奇怪字元導致錯誤
- 方法二：複製範本
  - 直接複製本專案中的 `.bat` 檔，重新命名後依需求修改內文
- 編碼與字碼頁注意
  - 本專案的 `.bat` 開頭有 `chcp 65001 >nul`，可在 UTF-8 環境下正確顯示中文
  - 若執行時出現亂碼，請改用 ANSI 或 UTF-8 無 BOM 重新存檔
- 常見問題
  - 雙擊執行無反應：確認副檔名為 `.bat`，不是 `.txt`
  - 找不到 Python：先安裝 Python 並勾選「Add Python to PATH」
  - API Key 未載入：確認 `.env` 與 `.bat` 在同一資料夾，且 `.env` 內有 `GOOGLE_API_KEY=你的金鑰`
- 安全提醒
  - 不要把實際的 API Key 寫進 `.bat`；請放在 `.env` 或系統環境變數

最小可用範例：
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
  echo 未設定 GOOGLE_API_KEY，請建立 .env 或設定系統環境變數
  pause & exit /b 1
)
set "VIDEO_URL=%~1"
if "%VIDEO_URL%"=="" (
  set /p VIDEO_URL=請輸入 YouTube 影片網址:
)
python youtube_summarizer_google_with_subtitle.py "%VIDEO_URL%"
pause
```

### 批次檔案使用（Windows）

#### 有字幕版本
1. 雙擊 `summarize_google_with_subtitle.bat`
2. 輸入 YouTube 影片網址
3. 等待處理完成

#### 無字幕版本
1. 雙擊 `summarize_google_no_subtitle.bat`
2. 輸入 YouTube 影片網址
3. 等待處理完成

### 參數說明
- `--language`: 指定字幕語言偏好（預設：zh-TW）
- 支援的網址格式：
  - `https://www.youtube.com/watch?v=VIDEO_ID`
  - `https://youtu.be/VIDEO_ID`
  - `VIDEO_ID`（直接輸入影片 ID）

## 輸出檔案

摘要會儲存為文字檔案，檔名格式：
- 有字幕版：`影片標題.txt`
- 無字幕版：`影片標題_無字幕版.txt`

檔案包含：
- 影片基本資訊
- 生成時間
- 使用的 AI 模型
- 詳細摘要內容

## 常見問題

### Q: 出現 "無法找到任何可用的字幕" 錯誤
**A:** 這表示影片沒有字幕，請使用無字幕版本：
```bash
python youtube_summarizer_google_no_subtitle.py "影片網址"
```

### Q: 出現 "請設定環境變數 GOOGLE_API_KEY" 錯誤
**A:** 請按照上述步驟設定 API Key，確保：
1. `.env` 檔案存在且格式正確
2. 或系統環境變數已正確設定
3. API Key 有效且未過期

### Q: 處理失敗或摘要品質不佳
**A:** 可能的原因：
1. 網路連線問題
2. API Key 額度不足
3. 影片內容過於複雜
4. 嘗試重新執行或使用不同的影片

### Q: 支援哪些語言的字幕？
**A:** 優先順序：繁體中文 > 簡體中文 > 英文 > 其他可用語言

## 技術規格

- **Python 版本**: 3.7+
- **AI 模型**: Google Gemini 2.0 Flash
- **最大處理長度**: 30,000 字元/區塊
- **支援格式**: YouTube 標準網址格式
- **輸出格式**: UTF-8 文字檔案

## 授權條款

本專案採用 MIT License，詳見 [LICENSE](LICENSE) 檔案。

## 貢獻

歡迎提交 Issue 和 Pull Request！

## 更新日誌

- v1.0.0: 初始版本，支援有字幕和無字幕兩種模式
