// Service Worker for iCoach App - v66 (β1.4.15 — detectArmSlot 근본 재수정)
const CACHE_NAME = 'icoach-v155';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './app.html',
  './manifest.json',
  './version.js',
  './ironarm.png',
  './icon_bug_report.png',
  './icon_legal.png',
  './icon_support.png',
  './icon_form.png',
  './icon_email.png',
  './fonts/SpoqaHanSansNeo-Regular.ttf',
  './fonts/SpoqaHanSansNeo-Bold.ttf',
  'https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Black+Han+Sans&display=swap'
];

// Install event - cache core assets
self.addEventListener('install', event => {
  console.log('Service Worker v10 installing...');
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS_TO_CACHE).catch(err => {
        console.log('Some assets failed to cache:', err);
        return Promise.resolve();
      });
    })
  );
  self.skipWaiting();
});

// Activate event - delete ALL old caches
self.addEventListener('activate', event => {
  console.log('Service Worker v10 activating...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch event - NETWORK-FIRST for HTML/JS, cache-first for images/fonts
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  if (event.request.method !== 'GET') return;

  // β1.2.5 — http/https 이외 스킴 무시 (chrome-extension://, data:, blob:, ws://, etc.)
  // Cache API 는 이들 스킴을 지원하지 않아 .put() 시 TypeError 폭주 → 메인 스레드 프리즈 유발
  if (url.protocol !== 'http:' && url.protocol !== 'https:') return;

  // Firebase/API - network only
  if (url.host.includes('firebase') || url.pathname.includes('/api/')) {
    event.respondWith(
      fetch(event.request).catch(() => {
        return caches.match(event.request).then(r => r || new Response(
          JSON.stringify({ offline: true, message: '오프라인 상태입니다' }),
          { status: 503, headers: { 'Content-Type': 'application/json' } }
        ));
      })
    );
    return;
  }

  // HTML, JS, JSON, manifest - NETWORK FIRST (always get latest)
  if (event.request.destination === 'document' ||
      url.pathname.endsWith('.html') ||
      url.pathname.endsWith('.js') ||
      url.pathname.endsWith('.json') ||
      url.pathname === '/' || url.pathname === './') {
    event.respondWith(
      fetch(event.request).then(response => {
        if (response.status === 200) {
          const cloned = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, cloned));
        }
        return response;
      }).catch(() => {
        return caches.match(event.request).then(r => r || caches.match('./app.html'));
      })
    );
    return;
  }

  // Images, fonts, CSS - cache first (with network fallback & update)
  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      // Return cache but also update in background
      const fetchPromise = fetch(event.request).then(networkResponse => {
        if (networkResponse && networkResponse.status === 200) {
          const cloned = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, cloned));
        }
        return networkResponse;
      }).catch(() => null);

      return cachedResponse || fetchPromise;
    })
  );
});

// Handle background sync
self.addEventListener('sync', event => {
  if (event.tag === 'sync-analyses') {
    event.waitUntil(Promise.resolve());
  }
});

// Message handler for skip waiting
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
