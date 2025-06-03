# M:\bmttnc-hutech-2280601703\lab-03\cipher\rsa\rsa_cipher.py

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import os

class RSACipher:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.keys_dir = os.path.join(os.path.dirname(__file__), 'keys')
        os.makedirs(self.keys_dir, exist_ok=True)
        self.private_key_path = os.path.join(self.keys_dir, 'private_key.pem')
        self.public_key_path = os.path.join(self.keys_dir, 'public_key.pem')

    def generate_keys(self):
        """Generates new RSA keys and saves them to files."""
        key = RSA.generate(2048)
        self.private_key = key
        self.public_key = key.publickey()

        with open(self.private_key_path, 'wb') as f:
            f.write(self.private_key.export_key('PEM'))
        with open(self.public_key_path, 'wb') as f:
            f.write(self.public_key.export_key('PEM'))
        print("RSA keys generated and saved.")

    def load_keys(self):
        """Loads RSA keys from files. Generates if not found."""
        if not os.path.exists(self.private_key_path) or \
           not os.path.exists(self.public_key_path):
            print("Keys not found, generating new ones...")
            self.generate_keys()
        else:
            with open(self.private_key_path, 'rb') as f:
                self.private_key = RSA.import_key(f.read())
            with open(self.public_key_path, 'rb') as f:
                self.public_key = RSA.import_key(f.read())
            print("RSA keys loaded.")
        return self.private_key, self.public_key

    def encrypt(self, message, public_key):
        """Encrypts a message using the public key."""
        cipher = PKCS1_OAEP.new(public_key)
        # Encode message to bytes before encryption
        return cipher.encrypt(message.encode('utf-8'))

    def decrypt(self, ciphertext, private_key):
        """Decrypts a ciphertext using the private key."""
        cipher = PKCS1_OAEP.new(private_key)
        # Decode the decrypted bytes back to string
        return cipher.decrypt(ciphertext).decode('utf-8')

    def sign(self, message, private_key):
        """Signs a message using the private key."""
        h = SHA256.new(message.encode('utf-8'))
        signer = PKCS1_v1_5.new(private_key)
        return signer.sign(h)

    def verify(self, message, signature, public_key):
        """Verifies a signature using the public key."""
        h = SHA256.new(message.encode('utf-8'))
        verifier = PKCS1_v1_5.new(public_key)
        return verifier.verify(h, signature)