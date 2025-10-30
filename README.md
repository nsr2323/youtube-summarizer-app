# 📺 YouTube Video Summarizer

> AI-powered YouTube video summarization tool with Progressive Web App support

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://nsr2323.github.io/youtube-summarizer-app/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[繁體中文](README_zh-TW.md) | English

## ✨ Features

- 🚀 **Instant Summaries**: Generate comprehensive video summaries in seconds
- 🎯 **Smart Subtitle Extraction**: Automatically fetches video subtitles in multiple languages
- 📱 **Progressive Web App**: Install on your mobile device for offline access
- 🔒 **Secure & Private**: API keys stored securely on Cloudflare Workers
- 🌍 **No Backend Required**: Serverless architecture powered by Cloudflare Workers
- 🎨 **Modern UI**: Beautiful, responsive design optimized for all devices

## 🎯 Quick Start

### For Users

1. Visit **[https://nsr2323.github.io/youtube-summarizer-app/](https://nsr2323.github.io/youtube-summarizer-app/)**
2. Paste any YouTube video URL
3. Click "🚀 生成摘要" (Generate Summary)
4. Wait for AI to analyze and generate the summary

### Install as PWA (Mobile)

1. Open the app in your mobile browser
2. Tap the browser menu
3. Select "Add to Home Screen"
4. Enjoy native app-like experience!

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────────┐         ┌─────────────────┐
│                 │         │                      │         │                 │
│  GitHub Pages   │────────▶│  Cloudflare Worker   │────────▶│  Google Gemini  │
│   (Frontend)    │         │   (API Proxy)        │         │      API        │
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

**Tech Stack:**
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Backend**: Cloudflare Workers (Serverless)
- **AI**: Google Gemini 2.0 Flash API
- **Hosting**: GitHub Pages + Cloudflare Workers

## 🛠️ For Developers

### Prerequisites

- Node.js 18+ and npm
- Cloudflare account
- Google AI Studio API key

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/nsr2323/youtube-summarizer-app.git
   cd youtube-summarizer-app
   ```

2. **Install Wrangler CLI**
   ```bash
   npm install -g wrangler
   wrangler login
   ```

3. **Configure API Key**
   ```bash
   cd gemini-proxy
   wrangler secret put GEMINI_API_KEY
   # Paste your Google AI Studio API key when prompted
   ```

4. **Deploy Worker**
   ```bash
   wrangler deploy
   ```

5. **Update Frontend**
   
   Edit `index.html` line 131 to use your Worker URL:
   ```javascript
   const WORKER_URL = 'https://your-worker.workers.dev';
   ```

6. **Deploy to GitHub Pages**
   ```bash
   git add .
   git commit -m "Deploy application"
   git push origin main
   ```
   
   Enable GitHub Pages in repository settings (Source: main branch, root folder)

### Local Development

1. **Test Worker locally**
   ```bash
   cd gemini-proxy
   wrangler dev
   ```

2. **Test Frontend**
   
   Use any local server (e.g., Python):
   ```bash
   python -m http.server 8000
   ```
   
   Open `http://localhost:8000` in your browser

## 📖 API Documentation

### Worker Endpoint

**POST** `https://your-worker.workers.dev`

**Request Body:**
```json
{
  "videoUrl": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
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

## 🔐 Security

- ✅ API keys stored as Cloudflare Worker secrets
- ✅ CORS properly configured
- ✅ No sensitive data in frontend code
- ✅ HTTPS enforced for all connections

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Google Gemini API](https://ai.google.dev/) for powerful AI capabilities
- [Cloudflare Workers](https://workers.cloudflare.com/) for serverless infrastructure
- [GitHub Pages](https://pages.github.com/) for free hosting

## 📧 Contact

Project Link: [https://github.com/nsr2323/youtube-summarizer-app](https://github.com/nsr2323/youtube-summarizer-app)

---

Made with ❤️ by the community
