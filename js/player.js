// Thin wrapper around the single <audio> element plus lock-screen controls (Media Session).
(function () {
  const audio = document.getElementById('audio');
  const MEDIA_ACTIONS = ['play', 'pause', 'seekbackward', 'seekforward', 'previoustrack', 'nexttrack', 'seekto'];
  let pendingStart = null; // seek requested before metadata was available

  audio.addEventListener('loadedmetadata', () => {
    if (pendingStart !== null) {
      audio.currentTime = Math.min(pendingStart, Math.max(0, audio.duration - 0.5));
      pendingStart = null;
    }
  });

  function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  }

  function load(src, { startAt = 0, rate = 1, volume = 1 } = {}) {
    pendingStart = startAt > 0 ? startAt : null;
    audio.src = src;
    audio.defaultPlaybackRate = rate;
    audio.playbackRate = rate;
    audio.volume = volume;
    audio.load();
  }

  function play() {
    // play() rejects if the browser blocks it or the source fails; the 'error' event reports the latter.
    return audio.play().catch(() => {});
  }

  function seek(time) {
    if (audio.readyState === 0) {
      pendingStart = Math.max(0, time);
      return;
    }
    const end = Number.isFinite(audio.duration) ? audio.duration : time;
    audio.currentTime = clamp(time, 0, end);
  }

  function setRate(rate) {
    audio.defaultPlaybackRate = rate;
    audio.playbackRate = rate;
  }

  function stop() {
    audio.pause();
    audio.removeAttribute('src');
    audio.load();
    pendingStart = null;
    if ('mediaSession' in navigator) {
      navigator.mediaSession.metadata = null;
      MEDIA_ACTIONS.forEach((action) => setActionHandler(action, null));
    }
  }

  function setActionHandler(action, handler) {
    try {
      navigator.mediaSession.setActionHandler(action, handler);
    } catch {
      /* action not supported by this browser */
    }
  }

  function setMediaSession({ title, album, artwork, onPrev, onNext }) {
    if (!('mediaSession' in navigator)) return;
    // Artwork must be http(s); skip it when the page is opened by double-click (file://).
    const canShowArtwork = location.protocol.startsWith('http');
    navigator.mediaSession.metadata = new MediaMetadata({
      title,
      album,
      artist: window.I18n.t('appName'),
      artwork: canShowArtwork ? [{ src: new URL(artwork, location.href).href, sizes: '600x800', type: 'image/svg+xml' }] : [],
    });
    setActionHandler('play', play);
    setActionHandler('pause', () => audio.pause());
    setActionHandler('seekbackward', () => seek(audio.currentTime - 10));
    setActionHandler('seekforward', () => seek(audio.currentTime + 10));
    setActionHandler('seekto', (details) => seek(details.seekTime));
    setActionHandler('previoustrack', onPrev || null);
    setActionHandler('nexttrack', onNext || null);
  }

  // Subscribes to an <audio> event and returns the unsubscribe function.
  function on(event, handler) {
    audio.addEventListener(event, handler);
    return () => audio.removeEventListener(event, handler);
  }

  window.Player = {
    load,
    play,
    pause: () => audio.pause(),
    toggle: () => (audio.paused ? play() : audio.pause()),
    seek,
    skip: (seconds) => seek((pendingStart ?? audio.currentTime) + seconds),
    setRate,
    setVolume: (volume) => {
      audio.volume = volume;
    },
    stop,
    setMediaSession,
    on,
    get currentTime() {
      return pendingStart ?? audio.currentTime;
    },
    get paused() {
      return audio.paused;
    },
    get ended() {
      return audio.ended;
    },
  };
})();
