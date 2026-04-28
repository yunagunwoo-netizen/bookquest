// ═══════════════════════════════════════════════════════
// BookQuest Service Worker
// ─────────────────────────────────────────────────────
// CACHE_NAME is bumped on every deploy by deploy_bookquest.ps1
// (it replaces `bookquest-v<ts>` with a fresh timestamp), so
// browsers detect sw.js bytes differ and install the new SW.
// ═══════════════════════════════════════════════════════
const CACHE_NAME = 'bookquest-v20260428080000';

// Only precache files that actually exist at repo root.
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './app.html',
  './manifest.json',
  './icons/app-icon-192.png',
  './icons/app-icon-512.png',
];

// install — precache then skip waiting so the new SW activates fast.
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

// activate — delete all stale caches, then take control of all tabs.
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

// fetch — HTML/JS/JSON: network-first. Images/fonts/CSS: stale-while-revalidate.
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);
  if (url.protocol !== 'http:' && url.protocol !== 'https:') return;

  // Firebase Cloud Functions / API — always network (503 when offline).
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

  // Documents / scripts / JSON — network-first, fall back to cache.
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

  // Images / fonts / CSS — cache-first + background update (SWR).
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

// index.html posts SKIP_WAITING when a new SW is installed — activate now.
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
