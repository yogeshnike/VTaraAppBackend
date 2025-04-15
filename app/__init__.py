from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {'message': 'API is running'}
        self.wfile.write(json.dumps(response).encode())

def create_app():
    return HTTPServer(('localhost', 5000), SimpleHTTPRequestHandler)
