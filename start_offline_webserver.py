import argparse
import http.server
import socketserver
import os

os.chdir('htdocs');

class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = http.server.SimpleHTTPRequestHandler.extensions_map.copy()
    extensions_map[''] = 'text/html'


parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=8000)
args = parser.parse_args()

host = "localhost"
with socketserver.TCPServer((host, args.port), Handler) as httpd:
    print(f"serving docs at http://{host}:{args.port}")
    httpd.serve_forever()
