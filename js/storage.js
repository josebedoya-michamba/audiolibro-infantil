// Listening progress and settings, kept in memory and mirrored to localStorage
// when it is available (private windows or blocked storage just lose persistence).
(function () {
  const PROGRESS_KEY = 'audiolibro:progress';
  const SETTINGS_KEY = 'audiolibro:settings';
  const DEFAULT_SETTINGS = { lang: null, speed: 1, volume: 1, textSize: 'm' };

  function read(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch {
      return fallback;
    }
  }

  function write(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch {
      /* storage unavailable: keep the in-memory copy */
    }
  }

  const progress = read(PROGRESS_KEY, {}) || {};
  const settings = { ...DEFAULT_SETTINGS, ...(read(SETTINGS_KEY, {}) || {}) };

  function bookProgress(bookId) {
    const saved = progress[bookId] || {};
    return {
      chapter: saved.chapter || 1,
      time: saved.time || 0,
      completed: Array.isArray(saved.completed) ? saved.completed : [],
    };
  }

  function savePosition(bookId, chapter, time) {
    const current = bookProgress(bookId);
    progress[bookId] = { ...current, chapter, time: Math.max(0, Math.round(time * 10) / 10) };
    write(PROGRESS_KEY, progress);
  }

  // Marks a chapter as listened and moves the bookmark to the start of the next one.
  function completeChapter(bookId, chapter, totalChapters) {
    const current = bookProgress(bookId);
    const completed = current.completed.includes(chapter) ? current.completed : [...current.completed, chapter];
    progress[bookId] = {
      chapter: chapter < totalChapters ? chapter + 1 : chapter,
      time: 0,
      completed: completed.sort((a, b) => a - b),
    };
    write(PROGRESS_KEY, progress);
  }

  function saveSettings(patch) {
    Object.assign(settings, patch);
    write(SETTINGS_KEY, settings);
  }

  window.Store = {
    bookProgress,
    savePosition,
    completeChapter,
    settings: () => ({ ...settings }),
    saveSettings,
  };
})();
