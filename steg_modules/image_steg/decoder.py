from PIL import Image
from steg_modules.crypto_utils import decrypt_message

def binary_to_message(binary_data):
    message = ''
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        message += chr(int(byte, 2))
        if message.endswith("<END>"):
            break
    return message.replace("<END>", '')

def decode_image(image_path, password=None):
    image = Image.open(image_path)
    binary_data = ''
    for pixel in image.getdata():
        for color in pixel[:3]:
            binary_data += str(color & 1)

    hidden_message = binary_to_message(binary_data)
    if password:
        try:
            hidden_message = decrypt_message(hidden_message, password)
        except:
            return "Incorrect password or corrupted message!"

    print("Hidden message extracted:")
    print(hidden_message)
    return hidden_message