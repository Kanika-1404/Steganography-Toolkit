from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import base64

def get_key(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

def encrypt_message(message, password):
    key = get_key(password)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')

def decrypt_message(ciphertext_b64, password):
    data = base64.b64decode(ciphertext_b64)
    key = get_key(password)
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
