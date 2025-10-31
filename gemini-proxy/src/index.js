export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const allowOrigin = '*';

    // CORS Preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': allowOrigin,
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Accept, X-Requested-With',
          'Access-Control-Max-Age': '86400',
        },
      });
    }

    if (request.method !== 'POST') {
      return new Response(JSON.stringify({ error: 'POST only' }), {
        status: 405,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': allowOrigin,
        },
      });
    }

    let bodyJson = {};
    try {
      bodyJson = await request.json();
    } catch (_) {}

    // 提取 YouTube 網址
    const videoUrl = bodyJson.videoUrl || bodyJson.contents?.[0]?.parts?.[0]?.text || '';
    
    try {
      // 從網址提取影片 ID
      const videoId = extractVideoId(videoUrl);
      if (!videoId) {
        return jsonResponse({ error: '無法從網址提取影片 ID，請提供有效的 YouTube 網址。' }, 400, allowOrigin);
      }

      // 取得影片基本資訊
      const videoInfo = await getVideoInfo(videoId);
      
      // 嘗試獲取字幕
      let transcript = '';
      try {
        transcript = await getTranscript(videoId);
      } catch (e) {
        // 無字幕時使用影片基本資訊
        transcript = `影片標題：${videoInfo.title}\n頻道：${videoInfo.author}\n描述：${videoInfo.description || '無描述'}`;
      }

      // 構建 Gemini 提示（繁體中文，要求結構化輸出）
      const prompt = `請以繁體中文為以下 YouTube 影片生成詳細且結構化的摘要。

影片資訊：
標題：${videoInfo.title}
頻道：${videoInfo.author}

${transcript.length > 100 ? '影片內容（可能為部分字幕）：\n' + transcript : transcript}

請使用以下 Markdown 格式提供摘要：

## 📋 概述
（2-3 句影片整體內容概述）

## ⭐ 重點
- 重點一
- 重點二
- 重點三（至少 3-5 個重點）

## 📖 詳細分析
（深入分析影片的主要內容和觀點，200-400 字）

## ⏱️ 關鍵時刻
- [時間] 關鍵時刻描述
- [時間] 關鍵時刻描述
（如果有時間資訊，請標註；如果沒有，可以描述重要轉折點）

## 💡 結論
（總結和建議）

請確保輸出完整的 Markdown 格式，包含所有區塊。摘要總長度：500-1000 字。`;

      // 調用 Gemini API
      const geminiUrl = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=' + env.GEMINI_API_KEY;
      
      const geminiPayload = {
        contents: [{ parts: [{ text: prompt }] }]
      };

      const upstream = await fetch(geminiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(geminiPayload),
      });

      const text = await upstream.text();
      
      if (!upstream.ok) {
        return jsonResponse({ error: 'Gemini API 錯誤', details: text }, upstream.status, allowOrigin);
      }

      // 解析 Gemini 回應並加入影片資訊
      let geminiData;
      try {
        geminiData = JSON.parse(text);
      } catch (e) {
        geminiData = { candidates: [{ content: { parts: [{ text: text }] } }] };
      }

      // 將影片資訊加入回應
      const response = {
        ...geminiData,
        videoInfo: {
          videoId: videoId,
          title: videoInfo.title,
          author: videoInfo.author,
          thumbnail: videoInfo.thumbnail,
          duration: videoInfo.duration,
          url: `https://www.youtube.com/watch?v=${videoId}`
        }
      };

      return new Response(JSON.stringify(response), {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': allowOrigin,
        },
      });

    } catch (error) {
      return jsonResponse({ error: error.message || '處理失敗' }, 500, allowOrigin);
    }
  },
};

// 輔助：提取 YouTube 影片 ID
function extractVideoId(url) {
  if (!url) return null;
  
  // 直接是 11 字元的 ID
  if (/^[a-zA-Z0-9_-]{11}$/.test(url)) return url;
  
  const patterns = [
    /(?:youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})/,
    /(?:youtu\.be\/)([a-zA-Z0-9_-]{11})/,
    /(?:youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})/,
    /(?:youtube\.com\/v\/)([a-zA-Z0-9_-]{11})/,
  ];
  
  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match) return match[1];
  }
  
  return null;
}

// 輔助：取得影片資訊
async function getVideoInfo(videoId) {
  try {
    const oembedUrl = `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${videoId}&format=json`;
    const resp = await fetch(oembedUrl);
    
    if (!resp.ok) {
      throw new Error('無法獲取影片資訊');
    }
    
    const data = await resp.json();
    // 構造高解析度縮圖 URL（maxresdefault，若不存在則使用 hqdefault）
    const thumbnailUrl = `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`;
    
    return {
      title: data.title || `影片 ${videoId}`,
      author: data.author_name || '未知頻道',
      thumbnail: thumbnailUrl,
      duration: null, // YouTube oEmbed 不提供時長，需使用 Data API
      description: data.description || ''
    };
   } catch (e) {
    return {
      title: `影片 ${videoId}`,
      author: '未知頻道',
      thumbnail: `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`,
      duration: null,
      description: ''
    };
  }
}

// 輔助：抓取字幕
async function getTranscript(videoId) {
  // 嘗試語言順序：繁中 -> 簡中 -> 英文
  const langs = ['zh-Hant', 'zh-TW', 'zh', 'en'];
  
  for (const lang of langs) {
    try {
      const timedtextUrl = `https://www.youtube.com/api/timedtext?v=${videoId}&lang=${lang}&fmt=json3`;
      const resp = await fetch(timedtextUrl);
      
      if (resp.ok) {
        const data = await resp.json();
        if (data.events && data.events.length > 0) {
          // 提取所有字幕文字
          const text = data.events
            .filter(e => e.segs)
            .map(e => e.segs.map(s => s.utf8).join(''))
            .join(' ')
            .trim();
          
          if (text.length > 50) {
            return text;
          }
        }
      }
    } catch (e) {
      // 繼續嘗試下一個語言
    }
  }
  
  throw new Error('無法獲取字幕');
}

// 輔助：JSON 回應
function jsonResponse(data, status, allowOrigin) {
  return new Response(JSON.stringify(data), {
    status: status,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': allowOrigin,
    },
  });
}


