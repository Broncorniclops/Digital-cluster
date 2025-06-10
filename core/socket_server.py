import socket
import threading

SOCKET_PATH = "/tmp/shutdown_ui.sock"
shutdown_flag_callback = None  # This will be assigned from Kivy UI

def handle_client(conn):
    try:
        data = conn.recv(1024).decode().strip()
        if data == "shutdown_pending" and shutdown_flag_callback:
            shutdown_flag_callback(True)
        elif data == "shutdown_clear" and shutdown_flag_callback:
            shutdown_flag_callback(False)
    finally:
        conn.close()

def start_socket_server():
    def server_loop():
        try:
            import os
            if os.path.exists(SOCKET_PATH):
                os.remove(SOCKET_PATH)
            server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            server.bind(SOCKET_PATH)
            server.listen(1)
            while True:
                conn, _ = server.accept()
                threading.Thread(target=handle_client, args=(conn,), daemon=True).start()
        except Exception as e:
            print(f"Socket server error: {e}")

    threading.Thread(target=server_loop, daemon=True).start()
