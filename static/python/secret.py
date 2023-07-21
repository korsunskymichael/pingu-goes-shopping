from cryptography.fernet import Fernet
from static.python.configs import *


class Secret:
    def __init__(self):
        self.cipher = Fernet(cipher_key)

    def decrypt_password(self, encrypted_password):
        decrypted_password = self.cipher.decrypt(encrypted_password)

        return decrypted_password.decode()

    def encrypt_password(self, password):
        message = password.encode()
        encrypted_password = self.cipher.encrypt(message)
        #print(encrypted_password.decode())

        return encrypted_password.decode()