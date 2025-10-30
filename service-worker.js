self.addEventListener('install', (e) => self.skipWaiting());
self.addEventListener('activate', (e) => clients.claim());

// 簡單示例：不攔截 .workers.dev API，避免影響 CORS/POST
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  if (url.hostname.endsWith('.workers.dev')) return;
  // 需要的話可在此加入靜態資源快取策略
});


