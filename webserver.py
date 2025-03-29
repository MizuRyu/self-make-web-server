import socket
from datetime import datetime
class WebServer:
    """
    Webサーバを表すクラス
    """
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

            response_body = self.get_body()
            response_header = self.get_header(response_body)
            response = f"{response_header}\r\n{response_body}".encode()

            client_socket.send(response)
            
            # コネクションを終了する
            client_socket.close()

        finally:
            print("=== Closing TCP Server ===")

    def get_header(self, response_body):
        """
        HTTPレスポンスヘッダを設定
        """
        header = ""
        header = "HTTP/1.1 200 OK\r\n"
        header += f"Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
        header += "Server: DemoServer\r\n"
        header += f"Content-Length: {len(response_body.encode())}\r\n"
        header += "Connecion: close\r\n"
        header += "Content-Type: text/html\r\n"
        return header
    
    def get_body(self):
        """
        HTTPレスポンスボディを設定
        """
        body = "<html><body><h1>Hello, World!</h1></body></html>"
        return body

if __name__ == "__main__":
    server = WebServer()
    server.serve()