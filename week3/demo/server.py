"""Local, deterministic htmx examples. Weather is fixture data, not a forecast."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', required=True, type=Path)
    parser.add_argument('--port', default=19363, type=int)
    args = parser.parse_args()
    htmx_source = (args.repo / 'src/htmx.js').read_bytes()
    page = Path(__file__).with_name('index.html').read_bytes()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            path = urlsplit(self.path).path
            if path == '/':
                status, mime, body = 200, 'text/html; charset=utf-8', page
            elif path == '/htmx.js':
                status, mime, body = 200, 'text/javascript', htmx_source
            elif path == '/weather':
                status, mime, body = 200, 'text/html; charset=utf-8', '<strong>Sunny · 22°C</strong><small>Local example data</small>'.encode()
            elif path == '/weather-unavailable':
                status, mime, body = 422, 'text/html; charset=utf-8', b'<strong>Weather temporarily unavailable</strong>'
            else:
                status, mime, body = 404, 'text/plain', b'Not found'
            self.send_response(status)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)

    print(f'Listening on http://127.0.0.1:{args.port}', flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()


if __name__ == '__main__':
    main()
