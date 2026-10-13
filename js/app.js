// Hash router and startup.
(function () {
  const app = document.getElementById('app');
  const routes = [
    [/^#?\/?$/, () => window.Views.library()],
    [/^#\/book\/([\w-]+)\/?$/, (id) => window.Views.book(id)],
    [/^#\/book\/([\w-]+)\/ch\/(\d+)\/?$/, (id, n) => window.Views.chapter(id, Number(n))],
  ];
  let view = null;
  let updateReady = false; // a new offline version took over; load it on the next screen change

  function resolve(hash) {
    if (!Array.isArray(window.BOOKS)) return window.Views.setup();
    for (const [pattern, make] of routes) {
      const match = hash.match(pattern);
      if (match) return make(...match.slice(1));
    }
    return window.Views.notFound();
  }

  function render() {
    view?.destroy?.();
    view = resolve(location.hash);
    app.replaceChildren(view.el);
    window.I18n.apply(app);
    document.title = view.title();
    window.scrollTo(0, 0);
    // Move focus to the new heading so screen readers announce the page change.
    view.el.querySelector('h1')?.focus({ preventScroll: true });
  }

  function syncLangButtons(lang) {
    document.querySelectorAll('[data-lang]').forEach((btn) => {
      btn.setAttribute('aria-pressed', String(btn.dataset.lang === lang));
    });
  }

  document.querySelector('.lang-switch').addEventListener('click', (event) => {
    const lang = event.target.closest('[data-lang]')?.dataset.lang;
    if (!lang || lang === window.I18n.getLang()) return;
    window.Store.saveSettings({ lang });
    window.I18n.setLang(lang);
  });

  window.I18n.onChange((lang) => {
    syncLangButtons(lang);
    if (view) document.title = view.title();
  });

  window.addEventListener('hashchange', () => (updateReady ? location.reload() : render()));

  // Offline: the service worker saves the whole app on the first visit. Only over
  // http(s) — a double-clicked index.html (file://) already works without internet.
  function setupOffline() {
    if (!('serviceWorker' in navigator) || !location.protocol.startsWith('http')) return;
    // Linked here instead of in index.html: file:// pages can't load it and log a CORS error.
    const manifest = document.createElement('link');
    manifest.rel = 'manifest';
    manifest.href = 'manifest.webmanifest';
    document.head.append(manifest);
    const status = document.querySelector('.offline-status');
    const show = (key, params) => {
      status.dataset.i18n = key;
      status.dataset.i18nParams = JSON.stringify(params || {});
      status.classList.toggle('is-ready', key === 'offlineReady');
      status.hidden = false;
      window.I18n.apply(status.parentElement);
    };
    // Progress only matters for the first download; updates arrive while the app already works offline.
    const hadController = Boolean(navigator.serviceWorker.controller);
    navigator.serviceWorker.addEventListener('message', (event) => {
      const data = event.data || {};
      if (data.type === 'offline-progress' && !hadController) {
        show('offlineSaving', { percent: Math.round((data.done / data.total) * 100) });
      }
      if (data.type === 'offline-ready') show('offlineReady');
    });
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      if (hadController) updateReady = true;
    });
    navigator.serviceWorker
      .register('sw.js', { updateViaCache: 'none' })
      .then(() => navigator.serviceWorker.ready)
      .then(() => show('offlineReady'))
      .catch(() => {});
    navigator.storage?.persist?.().catch(() => {});
  }

  const lang = window.I18n.initialLang(window.Store.settings().lang);
  window.I18n.setLang(lang);
  render();
  setupOffline();
})();
