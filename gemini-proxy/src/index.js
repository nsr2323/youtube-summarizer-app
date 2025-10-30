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

      // 構建 Gemini 提示（繁體中文）
      const prompt = `請以繁體中文為以下 YouTube 影片生成清晰且有條理的摘要。

影片資訊：
標題：${videoInfo.title}
頻道：${videoInfo.author}

${transcript.length > 100 ? '影片內容（可能為部分字幕）：\n' + transcript : transcript}

請提供：
1）影片高層次概述
2）3-5 個重點（以條列式呈現）
3）結論或建議

摘要長度：200-500 字。`;

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

      return new Response(text, {
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
    return {
      title: data.title || `影片 ${videoId}`,
      author: data.author_name || '未知頻道',
      description: ''
    };
  } catch (e) {
    return {
      title: `影片 ${videoId}`,
      author: '未知頻道',
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


