import socket

from workerthread import WorkerThread

class MultiThreadWebServer:
    """
    並列処理に対応したWebサーバ
    """

    def serve(self):
        """
        サーバを起動
        """

        print("=== Starting TCP Server ===")

        try:
            # サーバソケットの作成
            server_socket = self.create_server_socket()
            while True:
                print("=== [Server] Waiting for connection from the client===")
                (client_socket, address) = server_socket.accept()
                print(f"=== [Server] Connected from remote_addr: {address} ===")

                # WorkerThreadを生成してリクエストを処理する
                worker_thread = WorkerThread(client_socket, address)
                worker_thread.start()

        finally:
            # サーバを終了する
            print("=== Stopping Web Server ===")

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
    
if __name__ == "__main__":
    server = MultiThreadWebServer()
    server.serve()