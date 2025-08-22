#!/usr/bin/env python3
"""
Servidor de teste simples para verificar conectividade
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class TestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "message": "Teste de conectividade - Artell Backend",
                "status": "funcionando",
                "endpoint": "GET /"
            }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def do_POST(self):
        if self.path == '/test':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "message": "Teste POST funcionando",
                "received_data": post_data.decode('utf-8'),
                "status": "sucesso"
            }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def run_test_server(port=8002):
    server_address = ('', port)
    httpd = HTTPServer(server_address, TestHandler)
    print(f"🚀 Servidor de teste rodando em http://localhost:{port}")
    print(f"📱 Teste: http://localhost:{port}")
    print(f"🔄 Pressione Ctrl+C para parar")
    httpd.serve_forever()

if __name__ == '__main__':
    run_test_server()
