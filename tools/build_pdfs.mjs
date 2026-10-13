#!/usr/bin/env node
// Prints print.html?book=<id> to pdf/<id>.pdf for every book with headless Google
// Chrome, through the DevTools protocol (no npm packages needed). Run by tools/build.py.
// Set CHROME_PATH if Chrome is not in its usual place.
import { spawn } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const CHROME =
  process.env.CHROME_PATH ||
  [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  ].find((path) => existsSync(path));

if (!CHROME) {
  console.error('pdf/: Google Chrome not found (set CHROME_PATH)');
  process.exit(1);
}

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const books = JSON.parse(readFileSync(join(ROOT, 'content', 'stories.json'), 'utf8')).books;
const profile = mkdtempSync(join(tmpdir(), 'cuentos-pdf-'));
const chrome = spawn(
  CHROME,
  ['--headless=new', '--remote-debugging-port=0', `--user-data-dir=${profile}`, '--no-first-run', '--no-default-browser-check', 'about:blank'],
  { stdio: ['ignore', 'ignore', 'pipe'] }
);

try {
  // Chrome announces "DevTools listening on ws://127.0.0.1:<port>/..." on stderr.
  const port = await new Promise((resolve, reject) => {
    let output = '';
    chrome.stderr.on('data', (chunk) => {
      output += chunk;
      const match = output.match(/DevTools listening on ws:\/\/[^:]+:(\d+)\//);
      if (match) resolve(match[1]);
    });
    chrome.on('exit', () => reject(new Error('Chrome exited before starting')));
    setTimeout(() => reject(new Error('Chrome did not start in time')), 20000);
  });

  mkdirSync(join(ROOT, 'pdf'), { recursive: true });
  for (const book of books) {
    const target = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: 'PUT' })).json();
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    await new Promise((resolve) => ws.addEventListener('open', resolve, { once: true }));
    let nextId = 0;
    const pending = new Map();
    ws.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      if (message.id && pending.has(message.id)) {
        pending.get(message.id)(message);
        pending.delete(message.id);
      }
    });
    const send = (method, params = {}) =>
      new Promise((resolve) => {
        const id = ++nextId;
        pending.set(id, resolve);
        ws.send(JSON.stringify({ id, method, params }));
      });

    const url = `${pathToFileURL(join(ROOT, 'print.html')).href}?book=${encodeURIComponent(book.id)}`;
    await send('Page.enable');
    await send('Page.navigate', { url });
    let ready = false;
    for (let i = 0; i < 120 && !ready; i++) {
      await sleep(250);
      const result = await send('Runtime.evaluate', { expression: 'document.documentElement.dataset.ready', returnByValue: true });
      ready = result.result?.result?.value === 'true';
    }
    if (!ready) throw new Error(`${book.id}: print.html did not finish loading`);

    const pdf = await send('Page.printToPDF', { preferCSSPageSize: true, printBackground: true });
    if (!pdf.result) throw new Error(`${book.id}: ${pdf.error?.message || 'printToPDF failed'}`);
    const out = join(ROOT, 'pdf', `${book.id}.pdf`);
    writeFileSync(out, Buffer.from(pdf.result.data, 'base64'));
    console.log(`pdf/${book.id}.pdf: ${(readFileSync(out).length / 1024 / 1024).toFixed(1)} MB`);
    ws.close();
    await fetch(`http://127.0.0.1:${port}/json/close/${target.id}`);
  }
} finally {
  chrome.kill();
  await sleep(300);
  rmSync(profile, { recursive: true, force: true });
}
