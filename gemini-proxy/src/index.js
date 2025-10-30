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
      // Extract video ID from URL
      const videoId = extractVideoId(videoUrl);
      if (!videoId) {
        return jsonResponse({ error: 'Unable to extract video ID. Please provide a valid YouTube URL.' }, 400, allowOrigin);
      }

      // Fetch basic video info
      const videoInfo = await getVideoInfo(videoId);
      
      // 嘗試獲取字幕
      let transcript = '';
      try {
        transcript = await getTranscript(videoId);
      } catch (e) {
        // Fallback to basic info when no transcript available
        transcript = `Title: ${videoInfo.title}\nChannel: ${videoInfo.author}\nDescription: ${videoInfo.description || 'N/A'}`;
      }

      // Build Gemini prompt (English)
      const prompt = `Please generate a clear, well-structured summary in English for the following YouTube video.

Video Info:
Title: ${videoInfo.title}
Channel: ${videoInfo.author}

${transcript.length > 100 ? 'Transcript (may be partial):\n' + transcript : transcript}

Provide:
1) High-level overview of the video
2) 3-5 key takeaways as bullet points
3) A concluding insight or recommendation

Target length: 200-500 words.`;

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
        return jsonResponse({ error: 'Gemini API error', details: text }, upstream.status, allowOrigin);
      }

      return new Response(text, {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': allowOrigin,
        },
      });

    } catch (error) {
      return jsonResponse({ error: error.message || 'Processing failed' }, 500, allowOrigin);
    }
  },
};

// Helper: extract YouTube video ID
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

// Helper: fetch video info
async function getVideoInfo(videoId) {
  try {
    const oembedUrl = `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${videoId}&format=json`;
    const resp = await fetch(oembedUrl);
    
    if (!resp.ok) {
      throw new Error('Unable to fetch video info');
    }
    
    const data = await resp.json();
    return {
      title: data.title || `Video ${videoId}`,
      author: data.author_name || 'Unknown channel',
      description: ''
    };
  } catch (e) {
    return {
      title: `Video ${videoId}`,
      author: 'Unknown channel',
      description: ''
    };
  }
}

// Helper: fetch transcript
async function getTranscript(videoId) {
  // Try multiple languages (Traditional Chinese -> Simplified Chinese -> English)
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
  
  throw new Error('Unable to fetch transcript');
}

// Helper: JSON response
function jsonResponse(data, status, allowOrigin) {
  return new Response(JSON.stringify(data), {
    status: status,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': allowOrigin,
    },
  });
}


