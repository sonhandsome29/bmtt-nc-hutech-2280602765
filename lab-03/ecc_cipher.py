import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.ecc import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Kết nối các nút với các hàm xử lý API tương ứng
        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        """
        Gọi API để tạo cặp khóa ECC.
        Hiển thị thông báo thành công hoặc lỗi.
        """
        url = "http://127.0.0.1:5000/api/ecc/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"])
                msg.exec_() # Hiển thị hộp thoại thông báo
            else:
                print(f"Error while calling API: Status Code {response.status_code}")
                # Có thể hiển thị QMessageBox cho lỗi API không thành công
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(f"Error calling API: {response.status_code}")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            # Hiển thị QMessageBox cho lỗi kết nối
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Connection Error: {e}")
            msg.exec_()

    def call_api_sign(self):
        """
        Gọi API để ký một tin nhắn bằng khóa riêng.
        Hiển thị chữ ký và thông báo thành công hoặc lỗi.
        """
        url = "http://127.0.0.1:5000/api/ecc/sign"
        payload = {
            "message": self.ui.txt_info.toPlainText(), # Lấy tin nhắn từ trường văn bản
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_sign.setText(data["signature"]) # Đặt chữ ký vào trường văn bản
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully")
                msg.exec_()
            else:
                print(f"Error while calling API: Status Code {response.status_code}")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(f"Error calling API: {response.status_code}")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Connection Error: {e}")
            msg.exec_()

    def call_api_verify(self):
        """
        Gọi API để xác minh chữ ký của một tin nhắn bằng khóa công khai.
        Hiển thị thông báo xác minh thành công hoặc thất bại.
        """
        url = "http://127.0.0.1:5000/api/ecc/verify"
        payload = {
            "message": self.ui.txt_info.toPlainText(),    # Lấy tin nhắn từ trường văn bản
            "signature": self.ui.txt_sign.toPlainText() # Lấy chữ ký từ trường văn bản
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if (data["is_verified"]):
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verified Successfully")
                    msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verified Fail")
                    msg.exec_()
            else:
                print(f"Error while calling API: Status Code {response.status_code}")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(f"Error calling API: {response.status_code}")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Connection Error: {e}")
            msg.exec_()

# Điểm bắt đầu của ứng dụng
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
