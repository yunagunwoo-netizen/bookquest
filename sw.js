// ?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧??// BookQuest Service Worker
// ?????????????????????????????????????????????????????
// ?뵎 CACHE_NAME? 諛고룷???뚮쭏??deploy_bookquest.ps1 ??//    __TIMESTAMP__ ?먮━瑜??꾩옱 ?쒓컖?쇰줈 移섑솚?⑸땲??
//    ??留?而ㅻ컠留덈떎 sw.js 諛붿씠?멸? ?щ씪?몄꽌 釉뚮씪?곗?媛 ??SW濡?援먯껜.
// ?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧?먥븧??const CACHE_NAME = 'bookquest-v20260423120020';

// ?ㅼ젣濡?議댁옱?섎뒗 ?뚯씪留??꾨━罹먯떆 (install ??addAll)
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './version.js',
  './icon-192x192.png',
  './icon-512x512.png',
];

// install ??吏???먯궛 ?꾨━罹먯떆 ??利됱떆 ?쒖꽦???湲?嫄대꼫?곌린
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache =>
      cache.addAll(ASSETS_TO_CACHE).catch(err => {
        console.warn('[SW] precache partial fail:', err);
      })
    )
  );
  self.skipWaiting();
});

// activate ??援щ쾭??罹먯떆 ?꾨? ??젣 + 紐⑤뱺 ???μ븙
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(names =>
      Promise.all(
        names
          .filter(n => n !== CACHE_NAME)
          .map(n => caches.delete(n))
      )
    ).then(() => self.clients.claim())
  );
});

// fetch ??HTML/JS/JSON? ?ㅽ듃?뚰겕 ?곗꽑, 洹????대?吏쨌?고듃쨌CSS)??罹먯떆 ?곗꽑+諛깃렇?쇱슫??媛깆떊
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);
  if (url.protocol !== 'http:' && url.protocol !== 'https:') return;

  // Firebase Cloud Functions ??API????긽 ?ㅽ듃?뚰겕 (?ㅽ봽?쇱씤 ??503)
  if (url.host.includes('cloudfunctions') || url.pathname.includes('/api/')) {
    event.respondWith(
      fetch(event.request).catch(() =>
        new Response(JSON.stringify({ offline: true }), {
          status: 503,
          headers: { 'Content-Type': 'application/json' }
        })
      )
    );
    return;
  }

  // 臾몄꽌쨌?ㅽ겕由쏀듃쨌JSON ???ㅽ듃?뚰겕 ?곗꽑 (?ㅽ뙣 ??罹먯떆)
  if (
    event.request.destination === 'document' ||
    url.pathname.endsWith('.html') ||
    url.pathname.endsWith('.js') ||
    url.pathname.endsWith('.json') ||
    url.pathname === '/' ||
    url.pathname.endsWith('/')
  ) {
    event.respondWith(
      fetch(event.request)
        .then(resp => {
          if (resp && resp.status === 200) {
            const cloned = resp.clone();
            caches.open(CACHE_NAME).then(c => c.put(event.request, cloned));
          }
          return resp;
        })
        .catch(() =>
          caches.match(event.request).then(r => r || caches.match('./index.html'))
        )
    );
    return;
  }

  // ?대?吏쨌?고듃쨌CSS ??罹먯떆 ?곗꽑 + 諛깃렇?쇱슫??媛깆떊 (Stale-While-Revalidate)
  event.respondWith(
    caches.match(event.request).then(cached => {
      const fetchPromise = fetch(event.request)
        .then(resp => {
          if (resp && resp.status === 200) {
            const cloned = resp.clone();
            caches.open(CACHE_NAME).then(c => c.put(event.request, cloned));
          }
          return resp;
        })
        .catch(() => null);
      return cached || fetchPromise;
    })
  );
});

// index.html ?먯꽌 SKIP_WAITING 硫붿떆吏 蹂대궡硫?利됱떆 ?쒖꽦??self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
