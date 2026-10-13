// UI strings in Spanish and English. Story text stays in English.
(function () {
  const STRINGS = {
    es: {
      appName: 'Hora del Cuento',
      skipToContent: 'Saltar al contenido',
      language: 'Idioma',
      libraryTitle: '¿Qué cuento escuchamos hoy?',
      librarySubtitle: 'Elige un libro, ponte cómodo y escucha la historia capítulo por capítulo.',
      chapters: '{n} capítulos',
      minutes: '{n} min',
      statusNew: 'Nuevo',
      statusProgress: 'Vas por el capítulo {n}',
      statusDone: '¡Terminado!',
      backToLibrary: 'Biblioteca',
      audiobook: 'Audiolibro',
      start: 'Empezar a escuchar',
      continueChapter: 'Continuar · Capítulo {n}',
      listenAgain: 'Escuchar de nuevo',
      chapterN: 'Capítulo {n}',
      chapterOf: 'Capítulo {n} de {total}',
      chapterDoneLabel: 'Escuchado',
      player: 'Reproductor',
      play: 'Reproducir',
      pause: 'Pausar',
      back10: 'Retroceder 10 segundos',
      forward10: 'Adelantar 10 segundos',
      prevChapter: 'Capítulo anterior',
      nextChapter: 'Capítulo siguiente',
      position: 'Posición en el capítulo',
      speed: 'Velocidad',
      slow: 'Lento',
      normal: 'Normal',
      fast: 'Rápido',
      volume: 'Volumen',
      prevPage: 'Página anterior',
      nextPage: 'Página siguiente',
      pageOf: 'Página {n} de {total}',
      textSize: 'Tamaño de letra',
      sizeS: 'Letra pequeña',
      sizeM: 'Letra mediana',
      sizeL: 'Letra grande',
      sizeXL: 'Letra muy grande',
      resumed: 'Seguimos donde quedaste ({time})',
      chapterDone: '¡Capítulo terminado!',
      chapterDoneBody: '¿Seguimos con la historia?',
      bookDone: '¡Terminaste el libro!',
      bookDoneBody: 'Ya escuchaste todos los capítulos. ¡Muy bien!',
      nextChapterCta: 'Siguiente capítulo',
      chooseAnother: 'Elegir otro libro',
      audioError: 'No se pudo cargar el audio de este capítulo.',
      notFound: 'No encontramos ese cuento.',
      setupTitle: 'Faltan los audios',
      setupBody: 'Genera los audios y el archivo js/data.js desde la carpeta del proyecto:',
    },
    en: {
      appName: 'Story Time',
      skipToContent: 'Skip to content',
      language: 'Language',
      libraryTitle: 'Which story shall we hear today?',
      librarySubtitle: 'Pick a book, get cozy, and listen to the story one chapter at a time.',
      chapters: '{n} chapters',
      minutes: '{n} min',
      statusNew: 'New',
      statusProgress: 'You are on chapter {n}',
      statusDone: 'Finished!',
      backToLibrary: 'Library',
      audiobook: 'Audiobook',
      start: 'Start listening',
      continueChapter: 'Continue · Chapter {n}',
      listenAgain: 'Listen again',
      chapterN: 'Chapter {n}',
      chapterOf: 'Chapter {n} of {total}',
      chapterDoneLabel: 'Listened',
      player: 'Player',
      play: 'Play',
      pause: 'Pause',
      back10: 'Back 10 seconds',
      forward10: 'Forward 10 seconds',
      prevChapter: 'Previous chapter',
      nextChapter: 'Next chapter',
      position: 'Position in chapter',
      speed: 'Speed',
      slow: 'Slow',
      normal: 'Normal',
      fast: 'Fast',
      volume: 'Volume',
      prevPage: 'Previous page',
      nextPage: 'Next page',
      pageOf: 'Page {n} of {total}',
      textSize: 'Text size',
      sizeS: 'Small text',
      sizeM: 'Medium text',
      sizeL: 'Large text',
      sizeXL: 'Extra large text',
      resumed: 'Picking up where you left off ({time})',
      chapterDone: 'Chapter finished!',
      chapterDoneBody: 'Shall we keep going?',
      bookDone: 'You finished the book!',
      bookDoneBody: 'You listened to every chapter. Well done!',
      nextChapterCta: 'Next chapter',
      chooseAnother: 'Choose another book',
      audioError: "We couldn't load this chapter's audio.",
      notFound: "We couldn't find that story.",
      setupTitle: 'Audio files are missing',
      setupBody: 'Generate the audio and js/data.js from the project folder:',
    },
  };

  const listeners = [];
  let lang = 'es';

  function t(key, params) {
    let text = STRINGS[lang][key] ?? STRINGS.en[key] ?? key;
    for (const name in params || {}) text = text.replaceAll(`{${name}}`, params[name]);
    return text;
  }

  function paramsOf(el) {
    try {
      return el.dataset.i18nParams ? JSON.parse(el.dataset.i18nParams) : undefined;
    } catch {
      return undefined;
    }
  }

  // Fills every [data-i18n] text, [data-i18n-aria] label and [data-l10n-es/en] pair under root.
  function apply(root = document) {
    root.querySelectorAll('[data-i18n]').forEach((el) => {
      el.textContent = t(el.dataset.i18n, paramsOf(el));
    });
    root.querySelectorAll('[data-i18n-aria]').forEach((el) => {
      el.setAttribute('aria-label', t(el.dataset.i18nAria, paramsOf(el)));
    });
    root.querySelectorAll('[data-l10n-es]').forEach((el) => {
      el.textContent = lang === 'en' ? el.dataset.l10nEn : el.dataset.l10nEs;
    });
  }

  function setLang(next) {
    if (!STRINGS[next]) return;
    lang = next;
    document.documentElement.lang = next;
    apply();
    listeners.forEach((fn) => fn(next));
  }

  function initialLang(saved) {
    if (STRINGS[saved]) return saved;
    return (navigator.language || '').toLowerCase().startsWith('en') ? 'en' : 'es';
  }

  window.I18n = {
    t,
    apply,
    setLang,
    initialLang,
    getLang: () => lang,
    onChange: (fn) => listeners.push(fn),
  };
})();
