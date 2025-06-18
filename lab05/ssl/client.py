import socket
import ssl
import threading
import sys

# --- CẤU HÌNH CLIENT ---
HOST = 'localhost'
PORT = 12345
# Client cần file cert của server để xác thực
SERVER_CERT_FILE = './certificates/server-cert.crt'

def receive_messages(ssl_socket):
    """Chạy trên luồng riêng để nhận tin nhắn từ server."""
    while True:
        try:
            data = ssl_socket.recv(1024)
            if not data:
                break
            # Xử lý giao diện để không bị lẫn với dòng nhập liệu
            sys.stdout.write('\r' + ' ' * 60 + '\r') 
            print(data.decode('utf-8'))
            sys.stdout.write('> ')
            sys.stdout.flush()
        except (ssl.SSLError, ConnectionAbortedError):
            break
    print("\n🔌 Mất kết nối đến server.")

def main():
    """Hàm chính để kết nối và tương tác."""
    # Tạo SSL context, yêu cầu xác thực chứng chỉ của server
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_REQUIRED
    # Tải chứng chỉ của server để tin tưởng
    try:
        context.load_verify_locations(SERVER_CERT_FILE)
    except FileNotFoundError:
        print(f" Lỗi: Không tìm thấy tệp chứng chỉ '{SERVER_CERT_FILE}'.")
        return

    # Tạo socket và "bọc" bằng SSL
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_socket = context.wrap_socket(sock, server_hostname=HOST)

    try:
        ssl_socket.connect((HOST, PORT))
        print(f" Đã kết nối an toàn đến server {HOST}:{PORT}")

        # Hỏi người dùng biệt danh
        nickname = input("Nhập biệt danh của bạn để vào chat: ")
        print(f"Chào mừng {nickname}! Gõ 'exit' để thoát.")

        # Bắt đầu luồng nhận tin nhắn
        thread = threading.Thread(target=receive_messages, args=(ssl_socket,))
        thread.daemon = True
        thread.start()

        # Vòng lặp chính để gửi tin nhắn
        while thread.is_alive():
            message = input("> ")
            if message.lower() == 'exit':
                break
            
            # Gắn biệt danh vào trước tin nhắn
            full_message = f"[{nickname}]: {message}"
            ssl_socket.sendall(full_message.encode('utf-8'))
            
    except ssl.SSLCertVerificationError:
        print(f" Lỗi xác thực chứng chỉ. Chứng chỉ của server không hợp lệ hoặc không khớp.")
    except ConnectionRefusedError:
        print(" Kết nối bị từ chối. Server có đang chạy không?")
    except KeyboardInterrupt:
        print("\n Đang thoát...")
    except Exception as e:
        print(f" Lỗi không xác định: {e}")
    finally:
        ssl_socket.close()

if __name__ == "__main__":
    main()