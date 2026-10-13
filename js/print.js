// Printable version of one book (print.html?book=pip): a cover, one landscape
// page per paragraph with its scene and text, and a vocabulary page.
// tools/build_pdfs.mjs waits for <html data-ready="true"> and prints it to PDF.
(function () {
  const esc = (value) =>
    String(value).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const root = document.getElementById('book');
  const id = new URLSearchParams(location.search).get('book');
  const book = (window.BOOKS || []).find((b) => b.id === id);
  if (!book) {
    root.textContent = 'Book not found. Use print.html?book=<id>.';
    return;
  }

  document.title = book.title;
  document.body.classList.add(`theme-${book.theme}`);
  const vocabulary = window.Vocab.forBook(id);
  const footer = `<footer>${esc(book.title)} <span aria-hidden="true">·</span> <span class="page-number"></span></footer>`;
  const sheets = [];

  sheets.push(`
    <section class="sheet cover">
      <img class="cover-art" src="${esc(book.cover)}" alt="">
      <div class="cover-text">
        <p class="brand">Hora del Cuento · Story Time</p>
        <h1>${esc(book.title)}</h1>
        <p class="summary">${esc(book.summary.en)}</p>
        <p class="summary summary-es">${esc(book.summary.es)}</p>
        ${vocabulary ? `<p class="topic">Vocabulary: ${esc(vocabulary.topic.en)} · Vocabulario: ${esc(vocabulary.topic.es)}</p>` : ''}
        <ol class="contents">${book.chapters.map((ch) => `<li><span>Chapter ${ch.number}</span> ${esc(ch.title)}</li>`).join('')}</ol>
      </div>
    </section>`);

  for (const ch of book.chapters) {
    const scenes = window.SCENES?.[`${id}/${ch.number}`] || [];
    ch.paragraphs.forEach((paragraph, p) => {
      const text = paragraph.map((unit) => window.Vocab.markup(unit.text, id)).join(' ');
      sheets.push(`
        <section class="sheet page">
          <figure class="art"><img src="${esc(scenes[p] || ch.image)}" alt=""></figure>
          <div class="text">
            ${p === 0 ? `<header class="chapter"><p>Chapter ${ch.number}</p><h2>${esc(ch.title)}</h2></header>` : ''}
            <p class="story">${text}</p>
          </div>
          ${footer}
        </section>`);
    });
  }

  if (vocabulary) {
    sheets.push(`
      <section class="sheet vocabulary">
        <h2>Vocabulary <span>· Vocabulario</span></h2>
        <p class="topic">${esc(vocabulary.topic.en)} · ${esc(vocabulary.topic.es)}</p>
        <ul>${vocabulary.words
          .map((w) => `<li><span class="emoji">${esc(w.emoji || '')}</span><b>${esc(w.en)}</b><span class="es">${esc(w.es)}</span></li>`)
          .join('')}</ul>
        ${footer}
      </section>`);
  }

  root.innerHTML = sheets.join('');
  // The cover is page 1.
  root.querySelectorAll('.page-number').forEach((el, i) => {
    el.textContent = String(i + 2);
  });

  const images = [...root.querySelectorAll('img')].map((img) =>
    img.complete ? Promise.resolve() : new Promise((resolve) => (img.onload = img.onerror = resolve))
  );
  Promise.all([document.fonts.ready, ...images]).then(() => {
    document.documentElement.dataset.ready = 'true';
  });
})();
