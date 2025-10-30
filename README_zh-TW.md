# 📺 YouTube 影片摘要器

> 使用 AI 技術自動生成 YouTube 影片摘要，支援漸進式網頁應用程式 (PWA)

[![線上展示](https://img.shields.io/badge/展示-線上體驗-success)](https://nsr2323.github.io/youtube-summarizer-app/)
[![授權](https://img.shields.io/badge/授權-MIT-blue.svg)](LICENSE)

繁體中文 | [English](README.md)

## ✨ 特色功能

- 🚀 **即時摘要生成**：幾秒鐘內生成完整的影片摘要
- 🎯 **智慧字幕提取**：自動抓取多語言影片字幕
- 📱 **漸進式網頁應用**：可安裝到手機，支援離線使用
- 🔒 **安全私密**：API 金鑰安全存放在 Cloudflare Workers
- 🌍 **無需後端主機**：使用 Cloudflare Workers 無伺服器架構
- 🎨 **現代化介面**：美觀且響應式設計，適配所有裝置

## 🎯 快速開始

### 給一般使用者

1. 造訪 **[https://nsr2323.github.io/youtube-summarizer-app/](https://nsr2323.github.io/youtube-summarizer-app/)**
2. 貼上任何 YouTube 影片網址
3. 點擊「🚀 生成摘要」按鈕
4. 等待 AI 分析並生成摘要

### 安裝為 PWA（手機版）

1. 在手機瀏覽器中開啟應用程式
2. 點擊瀏覽器選單
3. 選擇「加到主畫面」
4. 享受如同原生 App 的使用體驗！

## 🏗️ 系統架構

```
┌─────────────────┐         ┌──────────────────────┐         ┌─────────────────┐
│                 │         │                      │         │                 │
│  GitHub Pages   │────────▶│  Cloudflare Worker   │────────▶│  Google Gemini  │
│   (前端網頁)     │         │   (API 代理)         │         │      API        │
│                 │         │                      │         │                 │
└─────────────────┘         └──────────────────────┘         └─────────────────┘
                                       │
                                       ▼
                            ┌──────────────────────┐
                            │                      │
                            │  YouTube oEmbed API  │
                            │  YouTube Timedtext   │
                            │                      │
                            └──────────────────────┘
```

**技術堆疊：**
- **前端**：原生 JavaScript、HTML5、CSS3
- **後端**：Cloudflare Workers（無伺服器）
- **AI 引擎**：Google Gemini 2.0 Flash API
- **託管服務**：GitHub Pages + Cloudflare Workers

## 🛠️ 給開發者

### 環境需求

- Node.js 18+ 和 npm
- Cloudflare 帳號
- Google AI Studio API 金鑰

### 安裝步驟

1. **複製專案**
   ```bash
   git clone https://github.com/nsr2323/youtube-summarizer-app.git
   cd youtube-summarizer-app
   ```

2. **安裝 Wrangler CLI**
   ```bash
   npm install -g wrangler
   wrangler login
   ```

3. **設定 API 金鑰**
   ```bash
   cd gemini-proxy
   wrangler secret put GEMINI_API_KEY
   # 在提示時貼上你的 Google AI Studio API 金鑰
   ```

4. **部署 Worker**
   ```bash
   wrangler deploy
   ```

5. **更新前端設定**
   
   編輯 `index.html` 第 131 行，使用你的 Worker 網址：
   ```javascript
   const WORKER_URL = 'https://your-worker.workers.dev';
   ```

6. **部署到 GitHub Pages**
   ```bash
   git add .
   git commit -m "部署應用程式"
   git push origin main
   ```
   
   在 GitHub 專案設定中啟用 GitHub Pages（來源：main 分支，根目錄）

### 本地開發

1. **測試 Worker**
   ```bash
   cd gemini-proxy
   wrangler dev
   ```

2. **測試前端**
   
   使用任何本地伺服器（例如 Python）：
   ```bash
   python -m http.server 8000
   ```
   
   在瀏覽器中開啟 `http://localhost:8000`

## 📖 API 文件

### Worker 端點

**POST** `https://your-worker.workers.dev`

**請求內容：**
```json
{
  "videoUrl": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**回應格式：**
```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "影片摘要內容..."
          }
        ]
      }
    }
  ]
}
```

## 🔐 安全性

- ✅ API 金鑰以 Cloudflare Worker 機密儲存
- ✅ 正確設定 CORS 跨域請求
- ✅ 前端程式碼不含敏感資料
- ✅ 所有連線強制使用 HTTPS

## 🎯 工作原理

1. **使用者輸入**：在網頁中貼上 YouTube 影片網址
2. **Worker 處理**：
   - 從網址提取影片 ID
   - 呼叫 YouTube oEmbed API 取得影片標題和頻道資訊
   - 嘗試抓取繁中/簡中/英文字幕
   - 若無字幕則使用影片基本資訊
3. **AI 分析**：將影片資訊送至 Gemini API 生成摘要
4. **回傳結果**：在網頁上顯示結構化的影片摘要

## 🤝 貢獻

歡迎提交 Pull Request！

1. Fork 此專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m '新增某個很棒的功能'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📝 授權

本專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 檔案

## 🙏 致謝

- [Google Gemini API](https://ai.google.dev/) 提供強大的 AI 能力
- [Cloudflare Workers](https://workers.cloudflare.com/) 提供無伺服器基礎架構
- [GitHub Pages](https://pages.github.com/) 提供免費託管服務

## 💡 常見問題

### Q: 為什麼有些影片無法生成摘要？

A: 部分影片可能沒有字幕或影片資訊受限。系統會在無法取得字幕時使用影片基本資訊進行摘要。

### Q: 支援哪些語言的字幕？

A: 系統會依序嘗試抓取：繁體中文 → 簡體中文 → 英文字幕。

### Q: API 金鑰安全嗎？

A: 是的。API 金鑰儲存在 Cloudflare Worker 的環境變數中，前端程式碼完全不會接觸到金鑰。

### Q: 可以離線使用嗎？

A: 安裝為 PWA 後，應用程式介面可離線使用，但生成摘要仍需網路連線。

## 📧 聯絡方式

專案連結：[https://github.com/nsr2323/youtube-summarizer-app](https://github.com/nsr2323/youtube-summarizer-app)

---

用 ❤️ 打造
