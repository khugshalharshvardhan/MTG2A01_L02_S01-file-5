"""Quiet local-only preview of the generated lesson (avoids filling a background log pipe)."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from pathlib import Path
import sys

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

class PreviewServer(ThreadingHTTPServer):
    # Two browser checks can request sprites, fonts and audio simultaneously.
    request_queue_size = 128
    daemon_threads = True

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1] / '3_BUILD'
    server = PreviewServer(('127.0.0.1', int(sys.argv[1]) if len(sys.argv)>1 else 8942),partial(QuietHandler,directory=str(root)))
    print('Preview: http://127.0.0.1:%d/MTG2A01_L02_S01.html' % server.server_port,flush=True)
    server.serve_forever()
