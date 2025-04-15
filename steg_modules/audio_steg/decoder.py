import wave
from steg_modules.crypto_utils import decrypt_message

def binary_to_message(binary_data):
    message = ''
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        message += chr(int(byte, 2))
        if message.endswith("<END>"):
            break
    return message.replace("<END>", '')

def decode_audio(stego_wav, password=None):
    with wave.open(stego_wav, 'rb') as audio:
        frames = bytearray(audio.readframes(audio.getnframes()))

    binary_data = ''.join([str(frame & 1) for frame in frames])
    hidden_message = binary_to_message(binary_data)

    if password:
        try:
            hidden_message = decrypt_message(hidden_message, password)
        except:
            return "Incorrect password or corrupted message!"

    print("Extracted message:")
    print(hidden_message)
    return hidden_message
