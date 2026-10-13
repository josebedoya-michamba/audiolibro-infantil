// Turns story text into HTML with the book's vocabulary words wrapped in
// <mark class="vocab"> (with the Spanish translation as a tooltip). Used by the
// chapter player and by print.html (PDF).
(function () {
  const escapeHTML = (value) =>
    String(value).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const escapeRegExp = (value) => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const matchers = {};

  function matcherFor(bookId) {
    if (!(bookId in matchers)) {
      const words = window.VOCABULARY?.[bookId]?.words || [];
      const byForm = new Map();
      words.forEach((word) => (word.forms || [word.en]).forEach((form) => byForm.set(form.toLowerCase(), word)));
      // Longest first so "raindrop" wins over "rain".
      const alternatives = [...byForm.keys()].sort((a, b) => b.length - a.length).map(escapeRegExp);
      matchers[bookId] = alternatives.length
        ? { regex: new RegExp(`\\b(?:${alternatives.join('|')})\\b`, 'gi'), byForm }
        : null;
    }
    return matchers[bookId];
  }

  function markup(text, bookId) {
    const matcher = matcherFor(bookId);
    if (!matcher) return escapeHTML(text);
    let html = '';
    let last = 0;
    for (const match of text.matchAll(matcher.regex)) {
      const word = matcher.byForm.get(match[0].toLowerCase());
      html += escapeHTML(text.slice(last, match.index));
      html += `<mark class="vocab" title="${escapeHTML(word.es)}">${escapeHTML(match[0])}</mark>`;
      last = match.index + match[0].length;
    }
    return html + escapeHTML(text.slice(last));
  }

  window.Vocab = { markup, forBook: (bookId) => window.VOCABULARY?.[bookId] };
})();
