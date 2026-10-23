// Offline support for the Strain Packs phone app.
// The game page is fetched fresh when there is signal (so updates arrive) and falls back to the saved copy offline.
const VERSION = "e653acda6b";
const CACHE = "strain-packs-" + VERSION;
const SHELL = ["./", "index.html", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png", "icons/maskable-512.png", "icons/apple-touch-icon.png", "icons/favicon-32.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith("strain-packs-") && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request; if (req.method !== "GET") return;
  const url = new URL(req.url);
  // the game page: network first, saved copy when offline
  // only the game's own page; other sites in this repo (like /pmarket-games/) load normally
  const scope = new URL(self.registration.scope).pathname;
  if (req.mode === "navigate" && url.origin === location.origin && url.pathname !== scope && url.pathname !== scope + "index.html") return;
  if (url.origin === location.origin && url.pathname.startsWith(scope + "pmarket-games/")) return;
  if (req.mode === "navigate"){
    e.respondWith(fetch(req).then(res => { const copy = res.clone(); caches.open(CACHE).then(c => c.put("index.html", copy)); return res; })
      .catch(() => caches.match("index.html").then(r => r || caches.match("./"))));
    return;
  }
  // fonts and the app's own files: saved copy first, then the network
  if (url.origin === location.origin || url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com"){
    e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(res => {
      if (res.ok || res.type === "opaque"){ const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
      return res;
    })));
  }
});
