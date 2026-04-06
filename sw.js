const CACHE_NAME = 'bookquest-v2';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icons/favicon.png',
  './icons/app-icon-192.png',
  './icons/app-icon-512.png',
  './covers/book1.jpg',
  './covers/book2.jpg',
  './covers/book3.jpg',
  './covers/book4.jpg',
  './covers/book5.jpg'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});
