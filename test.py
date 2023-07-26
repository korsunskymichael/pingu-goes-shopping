import base64

# Your byte string (example)
byte_string = b'widGvVVhNP7IlyanlsoVAcFTNb7XAvPhRxAEaQftSgA='


# Convert the byte string to Base64-encoded string
decoded_string = base64.urlsafe_b64encode(byte_string).decode('utf-8')

print("Decoded string:", decoded_string)

fernet_key = base64.urlsafe_b64decode(decoded_string)
print(fernet_key)
