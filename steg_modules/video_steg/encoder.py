import cv2
import os
import numpy as np
from steg_modules.crypto_utils import encrypt_message

def message_to_binary(message):
    return ''.join(format(ord(c), '08b') for c in message)

def encode_video(input_path, message, password=None):
    if password:
        message = encrypt_message(message, password)

    message += "<END>"
    binary_msg = message_to_binary(message)
    msg_idx = 0

    # Generate output path
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, base_name + "_stego.avi")

    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or np.isnan(fps):
        fps = 24

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or msg_idx >= len(binary_msg):
            break

        flat = frame.flatten()

        for i in range(len(flat)):
            if msg_idx < len(binary_msg):
                flat[i] = (flat[i] & ~1) | int(binary_msg[msg_idx])
                msg_idx += 1

        frame = flat.reshape(frame.shape)
        out.write(frame)

    # If any remaining frames are there, just write them as-is
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()
    print("Video encoded and saved to:", output_path)
    return output_path
