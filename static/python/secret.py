from cryptography.fernet import Fernet
import os


class Secret:
    def __init__(self):
        self.cipher = Fernet(os.environ.get("CIPHER_KEY"))

    def decrypt_password(self, encrypted_password):
        decrypted_password = self.cipher.decrypt(encrypted_password)

        return decrypted_password.decode()

    def encrypt_password(self, password):
        message = password.encode()
        encrypted_password = self.cipher.encrypt(message)

        return encrypted_password.decode()