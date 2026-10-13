// Hash router and startup.
(function () {
  const app = document.getElementById('app');
  const routes = [
    [/^#?\/?$/, () => window.Views.library()],
    [/^#\/book\/([\w-]+)\/?$/, (id) => window.Views.book(id)],
    [/^#\/book\/([\w-]+)\/ch\/(\d+)\/?$/, (id, n) => window.Views.chapter(id, Number(n))],
  ];
  let view = null;

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

  window.addEventListener('hashchange', render);

  const lang = window.I18n.initialLang(window.Store.settings().lang);
  window.I18n.setLang(lang);
  render();
})();
