# 🚀 Deployment Guide

This document explains how to deploy the YouTube Summarizer to production.

## 📋 Prerequisites

Make sure you have:

- ✅ GitHub account
- ✅ Cloudflare account (Free plan is enough)
- ✅ Google AI Studio API key
- ✅ Node.js 18+
- ✅ Git installed

## 🔑 Get a Google AI Studio API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in
3. Click “Get API Key”
4. Copy the generated key (format: `AIzaSy...`)
5. Keep it secret; do not commit it

## 📦 Step 1: Fork and Clone

```bash
git clone https://github.com/<your-username>/youtube-summarizer-app.git
cd youtube-summarizer-app
```

## ☁️ Step 2: Deploy Cloudflare Worker

### 2.1 Install Wrangler

```bash
npm install -g wrangler
```

### 2.2 Login to Cloudflare

```bash
wrangler login
```

### 2.3 First-time workers.dev subdomain

```bash
cd gemini-proxy
wrangler deploy
```

You’ll be asked to set a subdomain, resulting in:
```
https://gemini-proxy.<your-subdomain>.workers.dev
```

### 2.4 Set API key secret

```bash
wrangler secret put GEMINI_API_KEY
```

### 2.5 Verify

You should see a successful deploy message and a workers.dev URL.

## 🌐 Step 3: Configure Frontend

Edit `index.html` and set your Worker URL:

```javascript
const WORKER_URL = 'https://gemini-proxy.<your-subdomain>.workers.dev';
```

Commit the change:

```bash
git add index.html
git commit -m "chore: set Worker URL"
git push origin main
```

## 📄 Step 4: Enable GitHub Pages

1. Repository Settings → Pages
2. Source: “Deploy from a branch”
3. Branch: `main`
4. Folder: `/ (root)`
5. Save

GitHub Pages will build your site in 1–3 minutes.

## ✅ Step 5: Test

1. Open your GitHub Pages URL
2. Paste any YouTube URL (e.g. `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
3. Click “🚀 Generate Summary”
4. You should see a generated summary

## 📱 Step 6: Install as PWA (Mobile)

On your phone browser:

- iOS Safari: Share → Add to Home Screen
- Android Chrome: Menu → Add to Home screen

## 🔧 Advanced

### Custom domain
Set a CNAME in your DNS to point to `<username>.github.io` and configure Pages → Custom domain.

### Monitor Worker
```bash
wrangler tail
```

## 🐛 Troubleshooting

### “Failed to fetch” in frontend

1. Check `WORKER_URL` in `index.html`
2. Verify the Worker is deployed
3. Inspect the browser Network tab for details

### Wrong/expired API key

```bash
wrangler secret put GEMINI_API_KEY
wrangler deploy
```

### Pages 404

Ensure Pages is enabled and wait a few minutes. Check Actions logs if needed.

## 📊 Cost

| Service | Free tier | Typical usage |
| --- | --- | --- |
| GitHub Pages | 100 GB/mo | < 1 GB |
| Cloudflare Workers | 100k req/day | traffic-dependent |
| Google Gemini API | generous free tier | usage-dependent |

## 🎉 Done

You can now:

- 📱 Install the PWA
- 🔗 Share the link
- 🎨 Customize the UI
- 🚀 Extend features

See also: [README.md](README.md), [LICENSE](LICENSE), and the repo on GitHub.

