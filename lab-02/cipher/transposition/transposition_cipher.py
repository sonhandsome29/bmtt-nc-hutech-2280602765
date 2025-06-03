class TranspositionCipher:
    def __init__(self):
        pass

    def encrypt(self, text, key):
        encrypted_text = ''
        for col in range(key):
            pointer = col
            while pointer < len(text):
                encrypted_text += text[pointer]
                pointer += key
        return encrypted_text

    def decrypt(self, text, key):
        num_rows = key
        num_cols = int(len(text) / key) + (len(text) % key > 0)
        num_shaded_boxes = (num_cols * num_rows) - len(text)

        plaintext = [''] * num_cols
        col = 0
        row = 0

        for symbol in text:
            plaintext[col] += symbol
            col += 1
            if (col == num_cols) or (col == num_cols - 1 and row >= num_rows - num_shaded_boxes):
                col = 0
                row += 1

        return ''.join(plaintext)
