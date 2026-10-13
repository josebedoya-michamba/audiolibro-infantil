// Library, book and chapter views. Each view returns { el, title(), destroy? }.
(function () {
  const { t } = window.I18n;
  const SPEEDS = [
    { rate: 0.75, key: 'slow', emoji: '🐢' },
    { rate: 1, key: 'normal', emoji: '' },
    { rate: 1.25, key: 'fast', emoji: '🐇' },
  ];
  const TEXT_SIZES = [
    { size: 's', key: 'sizeS' },
    { size: 'm', key: 'sizeM' },
    { size: 'l', key: 'sizeL' },
    { size: 'xl', key: 'sizeXL' },
  ];
  const MAX_PAGE_SENTENCES = 2;
  const MAX_PAGE_WORDS = 28;
  const MIN_TEXT_PX = 18;
  const SENTENCE_END = /[.!?…]["”’)]*\s*$/;

  const esc = (value) =>
    String(value).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const params = (obj) => esc(JSON.stringify(obj));
  const icon = (id, cls = 'icon') => `<svg class="${cls}" aria-hidden="true"><use href="#i-${id}"/></svg>`;
  const reduceMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function formatTime(seconds) {
    const s = Math.max(0, Math.floor(seconds));
    return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
  }

  function fromHTML(html) {
    const template = document.createElement('template');
    template.innerHTML = html.trim();
    return template.content.firstElementChild;
  }

  function findBook(id) {
    return (window.BOOKS || []).find((book) => book.id === id);
  }

  function bookMinutes(book) {
    return Math.max(1, Math.round(book.chapters.reduce((sum, ch) => sum + ch.duration, 0) / 60));
  }

  function bookStatus(book) {
    const progress = window.Store.bookProgress(book.id);
    const done = progress.completed.length >= book.chapters.length;
    const started = progress.completed.length > 0 || progress.time > 0 || progress.chapter > 1;
    return { progress, state: done ? 'done' : started ? 'progress' : 'new' };
  }

  function bookMeta(book) {
    return `<span data-i18n="chapters" data-i18n-params="${params({ n: book.chapters.length })}"></span>
      <span aria-hidden="true">·</span>
      <span data-i18n="minutes" data-i18n-params="${params({ n: bookMinutes(book) })}"></span>`;
  }

  /* ---------- Library ---------- */

  function library() {
    const el = fromHTML(`
      <section class="library">
        <div class="library-intro">
          <h1 tabindex="-1" data-i18n="libraryTitle"></h1>
          <p class="lede" data-i18n="librarySubtitle"></p>
        </div>
        <ul class="shelf" role="list">
          ${window.BOOKS.map(shelfItem).join('')}
        </ul>
      </section>`);
    return { el, title: () => t('appName') };
  }

  function shelfItem(book, index) {
    const { progress, state } = bookStatus(book);
    const statusKey = { new: 'statusNew', progress: 'statusProgress', done: 'statusDone' }[state];
    const dots = book.chapters
      .map((ch) => `<span class="dot${progress.completed.includes(ch.number) ? ' is-filled' : ''}"></span>`)
      .join('');
    return `
      <li class="shelf-item theme-${esc(book.theme)}" style="--i:${index}">
        <a class="shelf-link" href="#/book/${esc(book.id)}">
          <span class="cover"><img src="${esc(book.cover)}" alt="" width="600" height="800"></span>
          <span class="shelf-title" lang="en">${esc(book.title)}</span>
          <span class="shelf-meta">${bookMeta(book)}</span>
          <span class="status status-${state}">
            <span class="dots" aria-hidden="true">${dots}</span>
            <span data-i18n="${statusKey}" data-i18n-params="${params({ n: progress.chapter })}"></span>
          </span>
        </a>
      </li>`;
  }

  /* ---------- Book ---------- */

  function book(id) {
    const book = findBook(id);
    if (!book) return notFound();
    const { progress, state } = bookStatus(book);
    const target = state === 'done' ? 1 : progress.chapter;
    const ctaKey = { new: 'start', progress: 'continueChapter', done: 'listenAgain' }[state];

    const steps = book.chapters
      .map((ch) => {
        const done = progress.completed.includes(ch.number);
        const current = state === 'progress' && ch.number === progress.chapter;
        return `
          <li class="step${done ? ' is-done' : ''}${current ? ' is-current' : ''}">
            <a class="step-link" href="#/book/${esc(book.id)}/ch/${ch.number}">
              <span class="step-dot" aria-hidden="true">${done ? icon('check') : ch.number}</span>
              <img class="step-thumb" src="${esc(ch.image)}" alt="" width="800" height="600" loading="lazy">
              <span class="step-text">
                <span class="step-label" data-i18n="chapterN" data-i18n-params="${params({ n: ch.number })}"></span>
                <span class="step-title" lang="en">${esc(ch.title)}</span>
              </span>
              <span class="step-time">
                ${done ? `<span class="visually-hidden" data-i18n="chapterDoneLabel"></span>` : ''}
                ${formatTime(ch.duration)}
              </span>
            </a>
          </li>`;
      })
      .join('');

    const el = fromHTML(`
      <section class="book-view theme-${esc(book.theme)}">
        <a class="back-link" href="#/">${icon('arrow-left')}<span data-i18n="backToLibrary"></span></a>
        <div class="book-layout">
          <div class="cover cover-large"><img src="${esc(book.cover)}" alt="" width="600" height="800"></div>
          <div class="book-info">
            <p class="eyebrow"><span data-i18n="audiobook"></span> <span aria-hidden="true">·</span> ${bookMeta(book)}</p>
            <h1 tabindex="-1" lang="en">${esc(book.title)}</h1>
            <p class="summary" data-l10n-es="${esc(book.summary.es)}" data-l10n-en="${esc(book.summary.en)}"></p>
            <a class="btn btn-primary btn-big" href="#/book/${esc(book.id)}/ch/${target}">
              ${icon(state === 'done' ? 'replay' : 'play')}
              <span data-i18n="${ctaKey}" data-i18n-params="${params({ n: target })}"></span>
            </a>
            <ol class="chapter-path" role="list">${steps}</ol>
          </div>
        </div>
      </section>`);
    return { el, title: () => `${book.title} · ${t('appName')}` };
  }

  /* ---------- Chapter + player ---------- */

  // Splits the chapter into book pages of one or two sentences (and at most MAX_PAGE_WORDS words).
  // Each unit is a narrated clip ({text, start}); dialogue tags like “Hello,” whispered Pip. span
  // several units, so units are first joined into sentences. Pages never cross paragraphs.
  function buildPages(paragraphs) {
    const pages = [];
    let index = 0;
    for (const paragraph of paragraphs) {
      const sentences = [];
      let sentence = [];
      for (const unit of paragraph) {
        sentence.push({ text: unit.text, start: unit.start, index: index++ });
        if (SENTENCE_END.test(unit.text)) {
          sentences.push(sentence);
          sentence = [];
        }
      }
      if (sentence.length) sentences.push(sentence);

      let page = [];
      let count = 0;
      let words = 0;
      for (const s of sentences) {
        const w = s.reduce((n, unit) => n + unit.text.split(/\s+/).length, 0);
        if (page.length && (count === MAX_PAGE_SENTENCES || words + w > MAX_PAGE_WORDS)) {
          pages.push(page);
          page = [];
          count = 0;
          words = 0;
        }
        page.push(...s);
        count += 1;
        words += w;
      }
      if (page.length) pages.push(page);
    }
    return pages;
  }

  function chapter(id, number) {
    const book = findBook(id);
    const ch = book && book.chapters[number - 1];
    if (!ch) return notFound();

    const total = book.chapters.length;
    const isLast = number === total;
    const settings = window.Store.settings();
    const saved = window.Store.bookProgress(id);
    const Player = window.Player;

    const pages = buildPages(ch.paragraphs);
    const starts = pages.flat().map((unit) => unit.start);
    const pageOf = [];
    pages.forEach((page, n) => page.forEach((unit) => (pageOf[unit.index] = n)));

    const speedButtons = SPEEDS.map(
      (s) => `<button type="button" class="chip" data-rate="${s.rate}" aria-pressed="${s.rate === settings.speed}">
          ${s.emoji ? `<span aria-hidden="true">${s.emoji}</span>` : ''}<span data-i18n="${s.key}"></span>
        </button>`
    ).join('');

    const sizeButtons = TEXT_SIZES.map(
      (s) => `<button type="button" class="size-btn" data-font="${s.size}" aria-pressed="${s.size === settings.textSize}" data-i18n-aria="${s.key}">A</button>`
    ).join('');

    const endAction = isLast
      ? `<a class="btn btn-primary" href="#/"><span data-i18n="chooseAnother"></span></a>`
      : `<a class="btn btn-primary" href="#/book/${esc(id)}/ch/${number + 1}"><span data-i18n="nextChapterCta"></span>${icon('next')}</a>`;

    const el = fromHTML(`
      <section class="chapter-view theme-${esc(book.theme)}">
        <a class="back-link" href="#/book/${esc(id)}">${icon('arrow-left')}<span lang="en">${esc(book.title)}</span></a>
        <div class="spread">
          <figure class="illustration"><img src="${esc(ch.image)}" alt="" width="800" height="600"></figure>
          <div class="book-page" data-text-size="${esc(settings.textSize)}">
            <header class="chapter-heading">
              <p class="eyebrow" data-i18n="chapterOf" data-i18n-params="${params({ n: number, total })}"></p>
              <h1 tabindex="-1" lang="en">${esc(ch.title)}</h1>
            </header>
            <div class="page-body">
              <div class="page-stage"><p class="page-text" lang="en"></p></div>
              <div class="page-nav">
                <button type="button" class="icon-btn page-turn" data-act="prev-page" data-i18n-aria="prevPage">${icon('arrow-left')}</button>
                <span class="page-dots" aria-hidden="true">${pages.map(() => '<span class="page-dot"></span>').join('')}</span>
                <span class="visually-hidden page-count"></span>
                <button type="button" class="icon-btn page-turn" data-act="next-page" data-i18n-aria="nextPage">${icon('arrow-right')}</button>
              </div>
            </div>
            <div class="end-card" hidden>
              <span class="end-star">${icon('star')}</span>
              <p class="end-title" data-i18n="${isLast ? 'bookDone' : 'chapterDone'}"></p>
              <p class="end-body" data-i18n="${isLast ? 'bookDoneBody' : 'chapterDoneBody'}"></p>
              <div class="end-actions">
                ${endAction}
                <button type="button" class="btn btn-ghost" data-act="replay">${icon('replay')}<span data-i18n="listenAgain"></span></button>
              </div>
            </div>
          </div>
        </div>
        <div class="player" role="region" data-i18n-aria="player">
          <div class="seek">
            <input class="seek-bar range" type="range" min="0" max="${ch.duration}" step="0.1" value="0" data-i18n-aria="position">
            <div class="times"><span class="t-now">0:00</span><span>${formatTime(ch.duration)}</span></div>
          </div>
          <div class="controls">
            <div class="speed pill-group" role="group" data-i18n-aria="speed">${speedButtons}</div>
            <div class="transport">
              <button type="button" class="icon-btn" data-act="prev" data-i18n-aria="prevChapter"${number === 1 ? ' disabled' : ''}>${icon('prev')}</button>
              <button type="button" class="icon-btn" data-act="back10" data-i18n-aria="back10">${icon('back10')}</button>
              <button type="button" class="play-btn" data-act="toggle" data-i18n-aria="play">${icon('play', 'icon icon-play')}${icon('pause', 'icon icon-pause')}</button>
              <button type="button" class="icon-btn" data-act="fwd10" data-i18n-aria="forward10">${icon('fwd10')}</button>
              <button type="button" class="icon-btn" data-act="next" data-i18n-aria="nextChapter"${isLast ? ' disabled' : ''}>${icon('next')}</button>
            </div>
            <div class="controls-end">
              <div class="text-size pill-group" role="group" data-i18n-aria="textSize">${sizeButtons}</div>
              <label class="volume">
                ${icon('volume')}
                <input class="range" type="range" min="0" max="1" step="0.05" value="${settings.volume}" data-i18n-aria="volume">
              </label>
            </div>
          </div>
          <p class="toast" role="status" aria-live="polite"></p>
        </div>
      </section>`);

    const $ = (selector) => el.querySelector(selector);
    const transport = $('.transport');
    const playBtn = $('.play-btn');
    const seekBar = $('.seek-bar');
    const timeNow = $('.t-now');
    const bookPage = $('.book-page');
    const pageBody = $('.page-body');
    const pageStage = $('.page-stage');
    const pageText = $('.page-text');
    const pageCount = $('.page-count');
    const prevPageBtn = $('[data-act="prev-page"]');
    const nextPageBtn = $('[data-act="next-page"]');
    const dots = [...el.querySelectorAll('.page-dot')];
    const endCard = $('.end-card');
    const toast = $('.toast');
    const volume = $('.volume input');
    const cleanups = [];
    let shownPage = -1;
    let current = -1;
    let raf = 0;
    let scrubbing = false;
    let played = false;
    let lastSaved = 0;
    let toastTimer = 0;

    const go = (n) => {
      location.hash = `#/book/${id}/ch/${n}`;
    };

    // Index of the last unit that has started at `time`.
    function unitAt(time) {
      let lo = 0;
      let hi = starts.length - 1;
      let found = 0;
      while (lo <= hi) {
        const mid = (lo + hi) >> 1;
        if (starts[mid] <= time + 0.05) {
          found = mid;
          lo = mid + 1;
        } else {
          hi = mid - 1;
        }
      }
      return found;
    }

    // The book keeps a fixed size: start from the chosen text size and shrink it
    // (binary search, down to MIN_TEXT_PX) until the page's text fits.
    function fitText() {
      pageText.style.fontSize = '';
      const style = getComputedStyle(pageStage);
      const available = pageStage.clientHeight - parseFloat(style.paddingTop) - parseFloat(style.paddingBottom);
      if (available <= 0 || pageText.offsetHeight <= available) return;
      let lo = MIN_TEXT_PX;
      let hi = parseFloat(getComputedStyle(pageText).fontSize);
      while (hi - lo > 0.5) {
        const mid = (lo + hi) / 2;
        pageText.style.fontSize = `${mid}px`;
        if (pageText.offsetHeight <= available) lo = mid;
        else hi = mid;
      }
      pageText.style.fontSize = `${lo}px`;
    }

    function showPage(n) {
      if (n === shownPage) return;
      const direction = n > shownPage ? 'next' : 'prev';
      const animate = shownPage !== -1;
      shownPage = n;
      current = -1;
      pageText.innerHTML = pages[n]
        .map((unit) => `<span class="sentence" data-i="${unit.index}">${esc(unit.text)}</span>`)
        .join(' ');
      fitText();
      dots.forEach((dot, i) => {
        dot.classList.toggle('is-active', i === n);
        dot.classList.toggle('is-past', i < n);
      });
      pageCount.dataset.i18nParams = JSON.stringify({ n: n + 1, total: pages.length });
      pageCount.dataset.i18n = 'pageOf';
      window.I18n.apply(pageCount.parentElement);
      prevPageBtn.disabled = n === 0;
      nextPageBtn.disabled = n === pages.length - 1;
      pageText.classList.remove('turn-next', 'turn-prev');
      if (animate) {
        void pageText.offsetWidth; // restart the page-turn animation
        pageText.classList.add(`turn-${direction}`);
      }
    }

    function highlight(index) {
      showPage(pageOf[index]);
      if (index === current) return;
      pageText.querySelector('.is-current')?.classList.remove('is-current');
      pageText.querySelector(`[data-i="${index}"]`)?.classList.add('is-current');
      current = index;
    }

    function render(time) {
      if (!scrubbing) seekBar.value = time;
      seekBar.style.setProperty('--fill', `${Math.min(100, (time / ch.duration) * 100)}%`);
      timeNow.textContent = formatTime(time);
      highlight(unitAt(time));
    }

    function tick() {
      render(Player.currentTime);
      raf = requestAnimationFrame(tick);
    }

    function turnTo(n) {
      const start = pages[n][0].start;
      Player.seek(start);
      render(start);
    }

    function save() {
      if (!played || Player.ended) return;
      window.Store.savePosition(id, number, Player.currentTime);
      lastSaved = Date.now();
    }

    function setPlaying(playing) {
      playBtn.classList.toggle('is-playing', playing);
      playBtn.dataset.i18nAria = playing ? 'pause' : 'play';
      window.I18n.apply(transport);
    }

    function setEnded(ended) {
      endCard.hidden = !ended;
      pageBody.hidden = ended;
      if (!ended) fitText();
    }

    function showToast(message) {
      toast.textContent = message;
      toast.classList.add('is-visible');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => toast.classList.remove('is-visible'), 3500);
    }

    function setVolumeFill() {
      volume.style.setProperty('--fill', `${volume.value * 100}%`);
    }

    // Audio events
    cleanups.push(
      Player.on('play', () => {
        played = true;
        setEnded(false);
        setPlaying(true);
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(tick);
      }),
      Player.on('pause', () => {
        setPlaying(false);
        cancelAnimationFrame(raf);
        render(Player.currentTime);
        save();
      }),
      Player.on('timeupdate', () => {
        if (Player.paused) render(Player.currentTime);
        if (Date.now() - lastSaved > 2000) save();
      }),
      Player.on('ended', () => {
        window.Store.completeChapter(id, number, total);
        render(ch.duration);
        setEnded(true);
      }),
      Player.on('error', () => showToast(t('audioError')))
    );

    // Controls
    el.addEventListener('click', (event) => {
      const sentence = event.target.closest('.sentence');
      if (sentence) {
        Player.seek(starts[Number(sentence.dataset.i)]);
        Player.play();
        return;
      }
      const rateBtn = event.target.closest('[data-rate]');
      if (rateBtn) {
        const rate = Number(rateBtn.dataset.rate);
        Player.setRate(rate);
        window.Store.saveSettings({ speed: rate });
        el.querySelectorAll('[data-rate]').forEach((b) => b.setAttribute('aria-pressed', String(b === rateBtn)));
        return;
      }
      const sizeBtn = event.target.closest('[data-font]');
      if (sizeBtn) {
        bookPage.dataset.textSize = sizeBtn.dataset.font;
        window.Store.saveSettings({ textSize: sizeBtn.dataset.font });
        el.querySelectorAll('[data-font]').forEach((b) => b.setAttribute('aria-pressed', String(b === sizeBtn)));
        fitText();
        return;
      }
      const action = event.target.closest('[data-act]')?.dataset.act;
      if (action === 'toggle') Player.toggle();
      else if (action === 'back10') Player.skip(-10);
      else if (action === 'fwd10') Player.skip(10);
      else if (action === 'prev-page' && shownPage > 0) turnTo(shownPage - 1);
      else if (action === 'next-page' && shownPage < pages.length - 1) turnTo(shownPage + 1);
      else if (action === 'prev' && number > 1) go(number - 1);
      else if (action === 'next' && !isLast) go(number + 1);
      else if (action === 'replay') {
        Player.seek(0);
        Player.play();
      }
    });

    seekBar.addEventListener('input', () => {
      scrubbing = true;
      Player.seek(Number(seekBar.value));
      render(Number(seekBar.value));
    });
    seekBar.addEventListener('change', () => {
      scrubbing = false;
    });

    volume.addEventListener('input', () => {
      Player.setVolume(Number(volume.value));
      setVolumeFill();
      window.Store.saveSettings({ volume: Number(volume.value) });
    });

    // Keyboard: Space = play/pause, ←/→ = previous/next page (unless a control has focus).
    const onKey = (event) => {
      if (event.altKey || event.ctrlKey || event.metaKey) return;
      const tag = event.target.tagName;
      if (event.key === ' ' && !['BUTTON', 'A', 'INPUT'].includes(tag)) {
        event.preventDefault();
        Player.toggle();
      } else if (event.key === 'ArrowLeft' && tag !== 'INPUT' && shownPage > 0) {
        event.preventDefault();
        turnTo(shownPage - 1);
      } else if (event.key === 'ArrowRight' && tag !== 'INPUT' && shownPage < pages.length - 1) {
        event.preventDefault();
        turnTo(shownPage + 1);
      }
    };
    const onHide = () => {
      if (document.visibilityState === 'hidden') save();
    };
    // Refit when the book is resized or the web fonts finish loading.
    const resizeObserver = new ResizeObserver(() => fitText());
    resizeObserver.observe(pageStage);
    document.fonts?.ready.then(() => fitText());
    document.addEventListener('keydown', onKey);
    document.addEventListener('visibilitychange', onHide);
    window.addEventListener('pagehide', save);
    cleanups.push(
      () => resizeObserver.disconnect(),
      () => document.removeEventListener('keydown', onKey),
      () => document.removeEventListener('visibilitychange', onHide),
      () => window.removeEventListener('pagehide', save)
    );

    // Start: resume where the child left off in this chapter.
    const startAt = saved.chapter === number && saved.time > 1 && saved.time < ch.duration - 2 ? saved.time : 0;
    Player.load(ch.audio, { startAt, rate: settings.speed, volume: settings.volume });
    Player.setMediaSession({
      title: ch.title,
      album: book.title,
      artwork: book.cover,
      onPrev: number > 1 ? () => go(number - 1) : null,
      onNext: isLast ? null : () => go(number + 1),
    });
    setVolumeFill();
    render(startAt);
    if (startAt) setTimeout(() => showToast(t('resumed', { time: formatTime(startAt) })), 300);

    return {
      el,
      title: () => `${ch.title} · ${book.title}`,
      destroy() {
        save();
        cancelAnimationFrame(raf);
        clearTimeout(toastTimer);
        cleanups.forEach((fn) => fn());
        Player.stop();
      },
    };
  }

  /* ---------- Fallbacks ---------- */

  function notFound() {
    const el = fromHTML(`
      <section class="notice">
        <h1 tabindex="-1" data-i18n="notFound"></h1>
        <a class="btn btn-primary" href="#/">${icon('arrow-left')}<span data-i18n="backToLibrary"></span></a>
      </section>`);
    return { el, title: () => t('appName') };
  }

  function setup() {
    const el = fromHTML(`
      <section class="notice">
        <h1 tabindex="-1" data-i18n="setupTitle"></h1>
        <p data-i18n="setupBody"></p>
        <pre><code>python3 -m venv .venv
.venv/bin/pip install -r tools/requirements.txt
.venv/bin/python tools/generate_audio.py</code></pre>
      </section>`);
    return { el, title: () => t('appName') };
  }

  window.Views = { library, book, chapter, notFound, setup };
})();
