import http.server
import socketserver
import os

os.chdir('htdocs');

class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = http.server.SimpleHTTPRequestHandler.extensions_map.copy()
    extensions_map[''] = 'text/html'


host = "localhost"
port = 8000
with socketserver.TCPServer((host, port), Handler) as httpd:
    print(f"serving docs at http://{host}:{port}")
    httpd.serve_forever()
