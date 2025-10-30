# 🤝 貢獻指南

感謝你考慮為 YouTube 影片摘要器做出貢獻！

## 📋 如何貢獻

### 回報問題

發現 Bug 或有功能建議？請遵循以下步驟：

1. 前往 [Issues](https://github.com/nsr2323/youtube-summarizer-app/issues)
2. 搜尋是否已有類似的 Issue
3. 如果沒有，點擊「New Issue」
4. 選擇適當的 Issue 類型
5. 填寫必要資訊

### 提交 Pull Request

1. **Fork 專案**
   ```bash
   # 在 GitHub 上點擊 Fork 按鈕
   git clone https://github.com/你的使用者名稱/youtube-summarizer-app.git
   cd youtube-summarizer-app
   ```

2. **建立新分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

3. **進行開發**
   - 遵循專案的程式碼風格
   - 撰寫清晰的提交訊息
   - 測試你的變更

4. **提交變更**
   ```bash
   git add .
   git commit -m "描述你的變更"
   git push origin feature/your-feature-name
   ```

5. **開啟 Pull Request**
   - 前往 GitHub 專案頁面
   - 點擊「Compare & pull request」
   - 填寫 PR 描述
   - 等待審核

## 📝 程式碼風格

### JavaScript

- 使用 2 空格縮排
- 使用單引號表示字串
- 函數名稱使用 camelCase
- 常數使用 UPPER_SNAKE_CASE

範例：
```javascript
const API_URL = 'https://api.example.com';

function fetchData(videoUrl) {
  return fetch(API_URL, {
    method: 'POST',
    body: JSON.stringify({ videoUrl }),
  });
}
```

### HTML/CSS

- 使用 2 空格縮排
- CSS class 名稱使用 kebab-case
- 保持語意化的 HTML 結構

## 🧪 測試

在提交 PR 前，請確保：

- ✅ 前端功能正常運作
- ✅ Worker 能正確處理請求
- ✅ 沒有 console 錯誤
- ✅ 手機版顯示正常
- ✅ PWA 功能正常

## 📖 文件

如果你的變更影響到使用方式，請更新：

- `README.md` - 功能說明
- `README_zh-TW.md` - 繁體中文版本
- `DEPLOYMENT.md` - 部署步驟（如有需要）

## 🎯 開發重點

### 前端（index.html）

- 保持簡潔的 UI
- 確保響應式設計
- 優化載入速度
- 提升無障礙性

### Worker（gemini-proxy/src/index.js）

- 處理錯誤情況
- 優化 API 呼叫
- 保護 API 金鑰
- 記錄必要的錯誤

## 🌟 功能建議

歡迎提出以下類型的改進：

### 優先級高
- 🔧 Bug 修復
- 🔒 安全性改進
- ♿ 無障礙性提升
- 📱 行動裝置體驗優化

### 優先級中
- ✨ 新功能
- 🎨 UI/UX 改進
- 📊 效能優化
- 🌍 多語言支援

### 優先級低
- 📝 文件改進
- 🧹 程式碼清理
- 🎭 視覺微調

## ❓ 需要協助？

不確定從哪裡開始？可以：

1. 查看標記為 `good first issue` 的 Issue
2. 閱讀專案的 [README.md](README.md)
3. 參考 [DEPLOYMENT.md](DEPLOYMENT.md) 了解架構
4. 在 Issue 中提問

## 📜 授權

提交 PR 即表示你同意將貢獻內容授權於 [MIT License](LICENSE)。

## 🙏 感謝

感謝所有貢獻者讓這個專案變得更好！

---

Happy Coding! 🚀

