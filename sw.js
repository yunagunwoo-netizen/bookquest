// ============================================================
// BookQuest Service Worker
// ------------------------------------------------------------
// CACHE_NAME is bumped on every deploy by deploy_bookquest.ps1
// (it replaces `bookquest-v<ts>` with a fresh timestamp), so
// browsers detect sw.js bytes differ and install the new SW.
// ============================================================
const CACHE_NAME = 'bookquest-v20260430161332';

// Only precache files that actually exist at repo root.
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './app.html',
  './app-data.js',
  './manifest.json',
  './icons/app-icon-192.png',
  './icons/app-icon-512.png',
];

// install: precache then skip waiting so the new SW activates fast.
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

// activate: delete all stale caches, then take control of all tabs.
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

// fetch: network/cache strategy, scoped strictly to same-origin GETs.
self.addEventListener('fetch', event => {
  // Only handle GET; POST/PUT/DELETE pass through untouched.
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Ignore chrome-extension:// and other non-http(s) protocols.
  if (url.protocol !== 'http:' && url.protocol !== 'https:') return;

  // CRITICAL: Do NOT intercept cross-origin requests.
  // Firestore / Firebase / Google APIs handle their own networking and
  // streaming connections (Listen channel). Letting the SW touch them
  // breaks responses with "Failed to convert value to 'Response'".
  if (url.origin !== self.location.origin) return;

  // Documents / scripts / JSON: network-first, fall back to cache.
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

  // Images / fonts / CSS: cache-first + background update (SWR).
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

// index.html posts SKIP_WAITING when a new SW is installed: activate now.
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
