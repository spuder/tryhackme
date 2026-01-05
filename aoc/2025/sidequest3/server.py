from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'hello world')
    
    def log_message(self, format, *args):
        pass

HTTPServer(('', 8000), Handler).serve_forever()
