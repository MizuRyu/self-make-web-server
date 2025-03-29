import os
import socket
from datetime import datetime


class WebServer:
    """
    Webサーバを表すクラス
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

    def serve(self):
        """
        サーバを起動
        """

        print("=== Starting TCP Server ===")

        try:
            # socketを作成
            server_socket = socket.socket()
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # socketをlocalhost:8080にバインド
            server_socket.bind(("localhost", 8080))
            server_socket.listen(10)

            print("=== Waiting for connection from the client===")
            (client_socket, address) = server_socket.accept()
            print(f"=== Connected from remote_addr: {address} ===")

            # クライアントからのリクエストデータを取得
            req_data = client_socket.recv(4096)

            # リクエストデータをファイルに書き出し
            with open("server_recv.txt", "wb") as f:
                f.write(req_data)


            static_file_path = self.parse_req(req_data.decode())

            try:
                # index.html読み込み
                with open(static_file_path, "rb") as f:
                    response_body = f.read()
                    
                response_header = self.build_header(200, len(response_body))

            except FileNotFoundError:
                # ファイルが見つからなかった場合は404を返す
                response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
                response_header = self.build_header(404, len(response_body))

            response = (response_header + "\r\n").encode() + response_body
            client_socket.send(response)
                
            # コネクションを終了する
            client_socket.close()

        finally:
            print("=== Closing TCP Server ===")

    def build_header(self, status_code, content_length):
        """
        HTTPレスポンスヘッダを設定
        """
        status_messages = {
            200: "OK",
            404: "Not Found",
        }
        reason = status_messages.get(status_code, "OK")
        header = (
            f"HTTP/1.1 {status_code} {reason}\r\n"
            f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
            "Server: DemoServer\r\n"
            f"Content-Length: {content_length}\r\n"
            "Connection: close\r\n"
            "Content-Type: text/html\r\n"
        )
        return header
    
    def parse_req(self, request):
        """
        リクエストデータをパースし、静的ファイルのパスをマッピング
        """
        req_lines, remain = request.split("\r\n", 1)
        req_header, req_body = remain.split("\r\n\r\n", 1)
        method, path, http_version = req_lines.split(" ", 2)
        # 相対パスに変換しておく
        relative_path = path.lstrip("/")
        static_file_path = os.path.join(self.STATIC_ROOT, relative_path)
        return static_file_path

if __name__ == "__main__":
    server = WebServer()
    server.serve()