# Hora del Cuento · Story Time

Audiolibros infantiles (6–9 años) con reproductor por capítulo. HTML, CSS y JavaScript puros, sin build.

- 3 cuentos originales en inglés, 3 capítulos cada uno, con ilustraciones SVG.
- Voces neuronales gratuitas generadas con [edge-tts](https://github.com/rany2/edge-tts): un narrador por libro y una voz por personaje.
- El capítulo se ve como un libro abierto: la ilustración a la izquierda y, a la derecha, el texto de una o dos oraciones a la vez. La página pasa sola mientras avanza el audio.
- Mientras suena el audio se resalta la frase actual; al tocar una frase, el audio salta a ella.
- Tamaño de letra ajustable (4 tamaños).
- Velocidad (lento / normal / rápido), volumen, ±10 s y capítulo anterior/siguiente.
- Guarda el progreso en el navegador: retoma el capítulo y el minuto donde quedó el niño.
- Interfaz en español o inglés, con selector.

## Ver la página

Abre `index.html` con doble clic, o sírvela localmente. Usa `tools/serve.py` y no `python3 -m http.server`: este último no soporta peticiones Range y sin eso no se puede saltar dentro del audio.

```sh
python3 tools/serve.py        # http://localhost:8000
```

Atajos de teclado en un capítulo: `Espacio` reproduce o pausa y `←` / `→` pasan a la página anterior o siguiente.

## Generar los audios

Los MP3 y `js/data.js` se generan a partir de `content/stories.json`:

```sh
python3 -m venv .venv
.venv/bin/pip install -r tools/requirements.txt
.venv/bin/python tools/generate_audio.py            # solo los capítulos que cambiaron
.venv/bin/python tools/generate_audio.py --force    # todo de nuevo
.venv/bin/python tools/generate_audio.py --book pip # un solo libro
```

El script sintetiza cada frase por separado y concatena los MP3. edge-tts entrega MP3 a 48 kbps constantes, así que el inicio de cada frase se calcula exacto a partir de los bytes; de ahí sale la sincronía del resaltado. `content/audio-cache.json` guarda esos tiempos para no volver a sintetizar lo que no cambió.

> **Nota (octubre 2026):** el servidor original de edge-tts devuelve 403. El script apunta la síntesis al endpoint que usa Edge 155 (ver [edge-tts#490](https://github.com/rany2/edge-tts/issues/490)). Cuando salga una versión de edge-tts con el arreglo, se puede borrar ese bloque de `tools/generate_audio.py`.

## Agregar o editar un cuento

1. En `content/stories.json`, agrega un libro con `id`, `title`, `theme` (`peach`, `sky`, `mint` o `lavender`), `summary` (es/en), `narrator`, `characters` y `chapters`.
2. Cada párrafo es una lista de segmentos:
   - Un texto simple lo lee el narrador.
   - Un objeto de una sola clave, como `{"Pip": "“Hello!”"}`, es un diálogo y lo lee la voz de ese personaje.
3. Pon las ilustraciones en `images/<id>/cover.svg` (3:4) y `images/<id>/ch1.svg`, `ch2.svg`… (4:3). Las actuales salen de `tools/make_illustrations.py`.
4. Corre `tools/generate_audio.py`.

Para ver las voces disponibles: `.venv/bin/edge-tts --list-voices`.

## Estructura

```
index.html            página única (router por hash)
css/styles.css        estilos (tokens pastel en :root)
js/i18n.js            textos ES/EN de la interfaz
js/storage.js         progreso y ajustes en localStorage
js/player.js          wrapper de <audio> + controles de pantalla de bloqueo
js/views.js           vistas: biblioteca, libro y capítulo
js/app.js             router y arranque
js/data.js            GENERADO: libros, capítulos, frases con tiempos
content/stories.json  FUENTE de los cuentos
audio/                GENERADO: MP3 por capítulo
images/               ilustraciones SVG
tools/                scripts de generación
```
