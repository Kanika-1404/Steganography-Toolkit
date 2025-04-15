import cv2
import numpy as np
from steg_modules.crypto_utils import decrypt_message

def binary_to_message(binary_data):
    chars = []
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        chars.append(chr(int(byte, 2)))
        if ''.join(chars).endswith("<END>"):
            break
    return ''.join(chars).replace("<END>", '')

def decode_video(video_path, password=None):
    cap = cv2.VideoCapture(video_path)
    binary_data = ''
    message = ''

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        flat = frame.flatten()
        binary_data += ''.join([str(pixel & 1) for pixel in flat])

        temp_msg = binary_to_message(binary_data)
        if "<END>" in temp_msg:
            message = temp_msg
            break

    cap.release()

    if password:
        try:
            message = decrypt_message(message, password)
        except:
            return "Incorrect password or corrupted message!"

    print("Extracted message from video:")
    print(message)
    return message
