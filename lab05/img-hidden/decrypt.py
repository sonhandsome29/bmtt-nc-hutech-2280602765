import sys
from PIL import Image

def decode_image(encoded_image_path):
    img = Image.open(encoded_image_path)
    width, height = img.size
    binary_message = ""

    # Trích xuất bit cuối cùng (LSB) từ mỗi kênh màu
    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))
            for color_channel in range(3):
                binary_message += format(pixel[color_channel], '08b')[-1]  # Lấy bit cuối cùng

    # Tách thông điệp dựa trên delimiter '1111111111111110'
    delimiter = '1111111111111110'
    if delimiter in binary_message:
        binary_message = binary_message[:binary_message.index(delimiter)]  # Cắt bỏ delimiter

    # Chuyển đổi nhị phân thành chuỗi ký tự
    message = ""
    for i in range(0, len(binary_message), 8):
        if i + 8 <= len(binary_message):
            byte = binary_message[i:i+8]
            char = chr(int(byte, 2))
            message += char
        else:
            break
    return message

def main():
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return

    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    print("Decoded message:", decoded_message)

if __name__ == "__main__":
    main()