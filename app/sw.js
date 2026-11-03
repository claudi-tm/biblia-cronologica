// Funcionamento offline. __VERSAO__ e __TEXTOS__ são preenchidos por scripts/montar.py.
const CACHE = "biblia-__VERSAO__";
const BASE = ["./", "index.html", "manifest.webmanifest", "icone-192.png", "icone-512.png"];
const TEXTOS = __TEXTOS__;

self.addEventListener("install", (e) => {
  // A página e os ícones primeiro; o texto bíblico (cerca de 4 MB) a seguir, sem bloquear.
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(BASE)).then(() => {
    caches.open(CACHE).then((c) => c.addAll(TEXTOS)).catch(() => {});
  }));
  self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))));
  self.clients.claim();
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  const fonte = url.hostname.endsWith("fonts.googleapis.com") || url.hostname.endsWith("fonts.gstatic.com");
  if (url.origin !== location.origin && !fonte) return;

  // Página: tenta a rede para trazer atualizações; sem rede, usa a cópia guardada.
  if (req.mode === "navigate") {
    e.respondWith(fetch(req).then((r) => {
      const copia = r.clone(); caches.open(CACHE).then((c) => c.put("index.html", copia)); return r;
    }).catch(() => caches.match("index.html")));
    return;
  }
  // Texto bíblico, ícones e letras: usa a cópia guardada; se não houver, vai à rede e guarda.
  e.respondWith(caches.match(req).then((hit) => hit || fetch(req).then((r) => {
    if (r.ok || r.type === "opaque") { const copia = r.clone(); caches.open(CACHE).then((c) => c.put(req, copia)); }
    return r;
  })));
});
