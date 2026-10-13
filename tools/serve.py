#!/usr/bin/env python3
"""Local web server with HTTP Range support.

`python3 -m http.server` ignores Range requests, so browsers can't seek inside
the MP3s (tapping a sentence or ±10 s would jump back to the start).

Usage:
    python3 tools/serve.py            # http://localhost:8000
    python3 tools/serve.py 8080       # another port
"""

import os
import re
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RANGE = re.compile(r"bytes=(\d*)-(\d*)")


class RangeRequestHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        self.range_length = None
        path = self.translate_path(self.path)
        match = RANGE.fullmatch(self.headers.get("Range", "").strip())
        if not match or not os.path.isfile(path):
            return super().send_head()

        size = os.path.getsize(path)
        first, last = match.groups()
        if first:
            start, end = int(first), min(int(last) if last else size - 1, size - 1)
        else:  # suffix range: the last N bytes
            start, end = max(0, size - int(last or 0)), size - 1
        if start > end:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.end_headers()
            return None

        file = open(path, "rb")
        file.seek(start)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        self.range_length = end - start + 1
        return file

    def copyfile(self, source, outputfile):
        try:
            if self.range_length is None:
                return super().copyfile(source, outputfile)
            remaining = self.range_length
            while remaining > 0:
                chunk = source.read(min(64 * 1024, remaining))
                if not chunk:
                    break
                outputfile.write(chunk)
                remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass  # the browser aborted the request (normal when seeking)

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    directory = sys.argv[2] if len(sys.argv) > 2 else str(ROOT)
    server = ThreadingHTTPServer(("127.0.0.1", port), partial(RangeRequestHandler, directory=directory))
    print(f"Serving {directory} at http://localhost:{port}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
