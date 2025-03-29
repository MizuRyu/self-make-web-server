import socket

class TCPClient:
    """
    TCP通信を行うクライアントを表すクラス
    """
    def request(self):
        """
        サーバへリクエストを送信
        """

        print("=== Starting TCP Client ===")

        try:
            # socketを作成
            client_socket = socket.socket()
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # サーバに接続
            print("=== Connecting to the server ===")
            client_socket.connect(("localhost", 80))
            print("=== Connected to the server ===")

            # リクエストデータをファイルから読み込む
            with open("client_send.txt", "rb") as f:
                req_data = f.read()
                print(req_data)

            # サーバへリクエストデータを送信
            client_socket.send(req_data)

            response = client_socket.recv(4096)

            # レスポンスデータをファイルに書き出し
            with open("client_recv.txt", "wb") as f:
                f.write(response)

            # コネクションを終了する
            client_socket.close()
        
        finally:
            print("=== Closing TCP Client ===")

if __name__ == "__main__":
    client = TCPClient()
    client.request()