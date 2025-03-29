import os
import re
import socket
from datetime import datetime
import traceback
from typing import Tuple, Optional, Match
from threading import Thread

import settings
from common.http.request import HTTPRequest
from common.http.response import HTTPResponse
from common.urls.urls import URL_VIEW, url_patterns
from common.urls.resolver import URLResolver

class Worker(Thread):
    # 拡張子とMIMEタイプのマッピング
    MIME_TYPES = {
        "html": "text/html; charset=utf-8",
        "css": "text/css",
        "js": "application/javascript",
        "png": "image/png",
        "jpg": "image/jpeg",
        "gif": "image/gif",
    }

    STATUS_LINES = {
        200: "200 OK",
        404: "404 Not Found",
        405: "405 Method Not Allowed",
    }

    def __init__(self, client_socket: socket, address: Tuple[str, int]):
        super().__init__()
        self.client_socket = client_socket
        self.address = address

    def run(self):
        """
        クライアントと接続済みのsocketを引数として受け取り、
        リクエストを処理してレスポンスを送信する
        """
        try:

            request_bytes = self.client_socket.recv(4096)

            # クライアントから送られてきたデータをファイルに書き出す
            with open("server_recv.txt", "wb") as f:
                f.write(request_bytes)

            request = self.parse_http_request(request_bytes)

            # URL解決
            view = URLResolver().resolve(request)
            
            # レスポンスを生成
            response = view(request)
                
            # レスポンスヘッダーを生成
            response_header = self.build_header(response, request)

            # レスポンス全体を生成
            response_bytes = (response_header + "\r\n").encode() + response.body
            
            # クライアントへレスポンスを送信
            self.client_socket.send(response_bytes)
        except Exception as e:
            print(f"=== [Worker] Error: {e} ===")
            traceback.print_exc()

        finally:
            print(f"=== [Worker] Closing connection to {self.address} ===")
            self.client_socket.close()


    def create_server_socket(self) -> socket:
        """
        通信を待ち受けるためのsocketを生成
        """        
        server_socket = socket.socket()
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # socketをlocalhost:8080にバインド
        server_socket.bind(("localhost", 8080))
        server_socket.listen(10)

        return server_socket

    def get_static_file_content(self, path: str) -> bytes:
        try:
            default_static_root = os.path.join(os.path.dirname(__file__), "../../static")
            static_root = getattr(settings, "STATIC_ROOT", default_static_root)
            relative_path = path.lstrip("/")
            static_file_path = os.path.join(static_root, relative_path)

            with open(static_file_path, "rb") as f:
                return f.read()
        except FileNotFoundError:
            raise
    def build_header(self, response: HTTPResponse, request: HTTPRequest) -> str:
        """
        HTTPレスポンスヘッダを設定
        """
        reason = self.STATUS_LINES.get(response.status_code, "OK")
        if response.content_type is None:
            if "." in request.path:
                extension = request.path.rsplit(".", maxsplit=1)[-1]
            else:
                extension = ""

            # 拡張子がない場合は、デフォルトのMIMEタイプを設定
            response.content_type = self.MIME_TYPES.get(extension, "application/octet-stream")
        header = (
            f"HTTP/1.1 {response.status_code} {reason}\r\n"
            f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
            "Server: DemoServer\r\n"
            f"Content-Length: {len(response.body)}\r\n"
            "Connection: close\r\n"
            f"Content-Type: {response.content_type}\r\n"
        )
        return header
    
    def parse_http_request(self, request) -> HTTPRequest:
        """
        リクエストデータをパースし、
        method: str,
        path: str,
        http_version: str,
        extension: str,
        request_header: dict,
        request_body: bytes
        に分割する
        """
        req_lines, remain = request.split(b"\r\n", 1)
        req_header, req_body = remain.split(b"\r\n\r\n", 1)
        method, path, http_version = req_lines.decode().split(" ")

        headers = {}
        for header_row in req_header.decode().split("\r\n"):
            if ": " in header_row:
                key, value = header_row.split(": ", 1)
                headers[key] = value

        return HTTPRequest(
            method=method,
            path=path,
            http_version=http_version,
            headers=headers,
            body=req_body
        )