# server.py (Đã cập nhật để hiển thị tin nhắn nhận được)
import socket
import ssl
import threading

# --- CẤU HÌNH SERVER ---
HOST = 'localhost'
PORT = 12345
CERT_FILE = './certificates/server-cert.crt'
KEY_FILE = './certificates/server-key.key'

# Danh sách để lưu các socket của client đã kết nối
clients = []
clients_lock = threading.Lock() # Lock để bảo vệ khi truy cập danh sách clients

def broadcast(message, source_socket):
    """Gửi tin nhắn đến tất cả các client, trừ client nguồn."""
    with clients_lock:
        for client_socket in clients:
            if client_socket != source_socket:
                try:
                    client_socket.sendall(message)
                except ssl.SSLError:
                    print(f"Lỗi gửi tin nhắn đến một client.")

def remove_client(client_socket):
    """Loại bỏ một client khỏi danh sách một cách an toàn."""
    with clients_lock:
        if client_socket in clients:
            clients.remove(client_socket)

def handle_client(ssl_client_socket):
    """Hàm xử lý cho mỗi client, chạy trên một luồng riêng."""
    peer_name = ssl_client_socket.getpeername()
    print(f" [KẾT NỐI MỚI] Từ {peer_name}")
    
    with clients_lock:
        clients.append(ssl_client_socket)
    
    try:
        while True:
            data = ssl_client_socket.recv(1024)
            if data:
                # --- DÒNG ĐƯỢC THÊM VÀO ---
                # In tin nhắn nhận được ra màn hình console của server
                print(f"<{peer_name}> {data.decode('utf-8')}")
                # -------------------------

                # Gửi dữ liệu nhận được đến tất cả các client khác
                broadcast(data, ssl_client_socket)
            else:
                break
    except (ssl.SSLError, ConnectionResetError):
        print(f" [LỖI KẾT NỐI] Kết nối với {peer_name} bị ngắt đột ngột.")
    except Exception as e:
        print(f" [LỖI KHÁC] {peer_name}: {e}")
    finally:
        print(f" [NGẮT KẾT NỐI] {peer_name} đã rời đi.")
        remove_client(ssl_client_socket)
        ssl_client_socket.close()

def main():
    """Hàm chính để khởi tạo và chạy server."""
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
    except OSError as e:
        print(f" Lỗi bind socket: {e}. Cổng {PORT} có thể đang được sử dụng.")
        return

    server_socket.listen(5)
    print(f" Server đang lắng nghe trên {HOST}:{PORT}...")

    try:
        while True:
            client_socket, _ = server_socket.accept()
            ssl_socket = context.wrap_socket(client_socket, server_side=True)
            thread = threading.Thread(target=handle_client, args=(ssl_socket,))
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        print("\n Đang tắt server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
