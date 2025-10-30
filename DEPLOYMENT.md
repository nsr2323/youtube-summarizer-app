# 🚀 部署指南

本文件說明如何將 YouTube 影片摘要器部署到生產環境。

## 📋 前置需求

在開始之前，請確保你已經準備好：

- ✅ GitHub 帳號
- ✅ Cloudflare 帳號（免費版即可）
- ✅ Google AI Studio API 金鑰（免費取得）
- ✅ Node.js 18 或更高版本
- ✅ Git 已安裝

## 🔑 取得 Google AI Studio API 金鑰

1. 前往 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登入你的 Google 帳號
3. 點擊「Get API Key」
4. 複製生成的 API 金鑰（格式：`AIzaSy...`）
5. ⚠️ 請妥善保管此金鑰，不要公開分享

## 📦 步驟 1：Fork 並複製專案

```bash
# 在 GitHub 上 Fork 此專案後，複製到本地
git clone https://github.com/你的使用者名稱/youtube-summarizer-app.git
cd youtube-summarizer-app
```

## ☁️ 步驟 2：部署 Cloudflare Worker

### 2.1 安裝 Wrangler CLI

```bash
npm install -g wrangler
```

### 2.2 登入 Cloudflare

```bash
wrangler login
```

這會開啟瀏覽器視窗，請授權 Wrangler 存取你的 Cloudflare 帳號。

### 2.3 註冊 Workers 子網域

如果這是你第一次使用 Cloudflare Workers，需要註冊一個子網域：

```bash
cd gemini-proxy
wrangler deploy
```

系統會提示你輸入子網域名稱（例如：`your-name`），完成後你的 Worker 網址會是：
```
https://gemini-proxy.你的子網域.workers.dev
```

### 2.4 設定 API 金鑰

```bash
wrangler secret put GEMINI_API_KEY
```

在提示時貼上你的 Google AI Studio API 金鑰，然後按 Enter。

### 2.5 確認部署成功

部署完成後，你會看到類似這樣的訊息：

```
✨ Deployed gemini-proxy to https://gemini-proxy.你的子網域.workers.dev
```

## 🌐 步驟 3：設定前端

### 3.1 更新 Worker URL

編輯專案根目錄的 `index.html` 檔案，找到第 131 行：

```javascript
const WORKER_URL = 'https://gemini-proxy.nsr2323.workers.dev';
```

將網址改為你的 Worker URL：

```javascript
const WORKER_URL = 'https://gemini-proxy.你的子網域.workers.dev';
```

### 3.2 提交變更

```bash
cd ..  # 回到專案根目錄
git add index.html
git commit -m "更新 Worker URL"
git push origin main
```

## 📄 步驟 4：啟用 GitHub Pages

1. 前往你的 GitHub 專案頁面
2. 點擊「Settings」（設定）
3. 在左側選單找到「Pages」
4. 在「Source」下拉選單中選擇「Deploy from a branch」
5. 選擇「main」分支
6. 選擇「/ (root)」資料夾
7. 點擊「Save」

### 等待部署

GitHub Pages 會自動部署你的網站，通常需要 1-3 分鐘。完成後，你會看到：

```
Your site is live at https://你的使用者名稱.github.io/youtube-summarizer-app/
```

## ✅ 步驟 5：測試

1. 開啟你的 GitHub Pages 網址
2. 貼上任何 YouTube 影片網址，例如：
   ```
   https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```
3. 點擊「🚀 生成摘要」
4. 等待幾秒鐘，應該會看到生成的摘要

## 📱 步驟 6：安裝為 PWA（手機版）

在手機瀏覽器中：

1. 開啟你的 GitHub Pages 網址
2. **iOS Safari**：點擊「分享」→「加入主畫面」
3. **Android Chrome**：點擊選單 →「加到主螢幕」
4. 現在你可以像使用原生 App 一樣使用這個工具了！

## 🔧 進階設定

### 自訂網域

如果你有自己的網域，可以在 GitHub Pages 設定中設定自訂網域：

1. 在 GitHub Pages 設定頁面找到「Custom domain」
2. 輸入你的網域（例如：`summarizer.yourdomain.com`）
3. 在你的 DNS 提供商設定 CNAME 記錄指向 `你的使用者名稱.github.io`

### 監控 Worker 使用量

Cloudflare 免費方案提供：
- 每天 100,000 次請求
- 10ms CPU 時間/請求

查看使用量：
```bash
wrangler tail
```

## 🐛 疑難排解

### Worker 部署失敗

```bash
# 確認 Wrangler 已登入
wrangler whoami

# 重新登入
wrangler logout
wrangler login
```

### 前端顯示 "Failed to fetch"

1. 檢查 `index.html` 中的 `WORKER_URL` 是否正確
2. 確認 Worker 已成功部署
3. 在瀏覽器開發者工具查看 Network 面板的錯誤訊息

### API 金鑰錯誤

```bash
# 重新設定 API 金鑰
cd gemini-proxy
wrangler secret put GEMINI_API_KEY
wrangler deploy
```

### GitHub Pages 404 錯誤

1. 確認 GitHub Pages 已啟用
2. 等待 3-5 分鐘讓 GitHub 完成部署
3. 檢查專案設定中的 Actions 分頁，確認部署成功

## 📊 成本估算

這個專案可以**完全免費**運行：

| 服務 | 免費額度 | 估計使用量 |
|------|---------|-----------|
| GitHub Pages | 100 GB/月 | < 1 GB |
| Cloudflare Workers | 100,000 請求/天 | 取決於流量 |
| Google Gemini API | 1,500 請求/天 | 取決於使用 |

## 🎉 完成！

恭喜你成功部署了 YouTube 影片摘要器！現在你可以：

- 📱 在手機上安裝 PWA
- 🔗 分享連結給朋友
- 🎨 自訂 UI 樣式
- 🚀 擴充更多功能

## 📚 後續步驟

- 閱讀 [README.md](README.md) 了解更多功能
- 查看 [LICENSE](LICENSE) 了解授權資訊
- 貢獻程式碼到 [GitHub](https://github.com/nsr2323/youtube-summarizer-app)

---

需要協助？請在 GitHub 專案中開啟 Issue！

