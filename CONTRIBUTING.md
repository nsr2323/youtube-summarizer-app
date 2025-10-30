# 🤝 Contributing Guide

Thank you for considering contributing to the YouTube Summarizer project!

## 📋 How to Contribute

### Report Issues

Found a bug or have a feature request? Please:

1. Go to [Issues](https://github.com/nsr2323/youtube-summarizer-app/issues)
2. Search existing issues first
3. If none, click “New issue” and provide details

### Submit a Pull Request

1. **Fork the repository**
   ```bash
   git clone https://github.com/<your-username>/youtube-summarizer-app.git
   cd youtube-summarizer-app
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Develop**
   - Follow the code style
   - Write clear commit messages
   - Test your changes

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Describe your change"
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request**
   - Go to the repository on GitHub
   - Click “Compare & pull request”
   - Fill in the description and submit

## 📝 Code Style

### JavaScript

- 2-space indentation
- Single quotes for strings
- Functions in camelCase
- Constants in UPPER_SNAKE_CASE

Example:
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

- 2-space indentation
- CSS class names in kebab-case
- Semantic HTML structure

## 🧪 Testing

Before submitting a PR, ensure:

- ✅ Frontend works without errors
- ✅ Worker handles requests correctly
- ✅ No console errors
- ✅ Mobile layout looks good
- ✅ PWA works as expected

## 📖 Documentation

If your change affects usage, please update:

- `README.md` – main guide
- `README_zh-TW.md` – Traditional Chinese version (optional)
- `DEPLOYMENT.md` – deployment steps if needed

## 🎯 Focus Areas

### Frontend (`index.html`)

- Keep UI simple and responsive
- Optimize loading performance
- Improve accessibility

### Worker (`gemini-proxy/src/index.js`)

- Robust error handling
- Efficient API calls
- Keep API key secure
- Log meaningful errors

## 🌟 Suggestions

High priority:
- 🔧 Bug fixes
- 🔒 Security improvements
- ♿ Accessibility improvements
- 📱 Mobile UX improvements

Medium priority:
- ✨ New features
- 🎨 UI/UX improvements
- 📊 Performance
- 🌍 i18n / l10n

Low priority:
- 📝 Docs improvements
- 🧹 Code cleanup
- 🎭 Visual polish

## ❓ Need Help?

Start with:

1. Issues labeled `good first issue`
2. The [README.md](README.md)
3. The [DEPLOYMENT.md](DEPLOYMENT.md)
4. Asking questions in Issues

## 📜 License

By submitting a PR you agree to license your contributions under the [MIT License](LICENSE).

## 🙏 Thanks

Thanks to all contributors for making this project better!

---

Happy Coding! 🚀

