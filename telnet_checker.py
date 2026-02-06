#!/usr/bin/env python3
import sys
import socket
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import threading

class TelnetCheckerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Парсим URL для получения параметров
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        # Проверяем наличие необходимых параметров
        if 'ip' not in query_params or 'port' not in query_params:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Missing parameters. Use: /check?ip=X.X.X.X&port=YYYY'}
            self.wfile.write(json.dumps(response).encode())
            return
        
        ip_address = query_params['ip'][0]
        port = query_params['port'][0]
        
        # Валидация порта
        try:
            port = int(port)
            if not (1 <= port <= 65535):
                raise ValueError
        except ValueError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Invalid port number. Port must be between 1 and 65535'}
            self.wfile.write(json.dumps(response).encode())
            return
        
        # Проверяем подключение
        result = self.check_telnet(ip_address, port)
        
        # Формируем ответ
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            'ip': ip_address,
            'port': port,
            'status': result,
            'message': 'Connection successful' if result == 1 else 'Connection failed'
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def check_telnet(self, ip_address, port, timeout=5):
        """Проверяет доступность TCP порта"""
        try:
            # Создаем сокет с таймаутом
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            # Пытаемся подключиться
            result = sock.connect_ex((ip_address, port))
            sock.close()
            
            # 0 означает успешное подключение
            return 1 if result == 0 else 0
            
        except socket.timeout:
            return 0
        except socket.error as e:
            print(f"Socket error: {e}", file=sys.stderr)
            return 0
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return 0
    
    def log_message(self, format, *args):
        # Отключаем стандартное логирование запросов
        pass

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, TelnetCheckerHandler)
    print(f"Server started on port {port}")
    print(f"Usage: http://localhost:{port}/check?ip=X.X.X.X&port=YYYY")
    httpd.serve_forever()

if __name__ == '__main__':
    # Получаем порт из аргументов командной строки или используем по умолчанию
    server_port = 8080
    if len(sys.argv) > 1:
        try:
            server_port = int(sys.argv[1])
        except ValueError:
            print("Invalid port. Using default port 8080")
    
    run_server(server_port)