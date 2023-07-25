from cryptography.fernet import Fernet
import os
import base64

fernet_key_string = os.environ.get("CIPHER_KEY")
fernet_key = base64.urlsafe_b64decode(fernet_key_string)


class Secret:
    def __init__(self):
        self.cipher = Fernet(fernet_key)

    def decrypt_password(self, encrypted_password):
        decrypted_password = self.cipher.decrypt(encrypted_password)

        return decrypted_password.decode()

    def encrypt_password(self, password):
        message = password.encode()
        encrypted_password = self.cipher.encrypt(message)

        return encrypted_password.decode()