import socket

class TCPServer:
    """
    TCP通信を行うサーバーを表すクラス
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
            
            # コネクションを終了する
            client_socket.close()

        finally:
            print("=== Closing TCP Server ===")

if __name__ == "__main__":
    server = TCPServer()
    server.serve()