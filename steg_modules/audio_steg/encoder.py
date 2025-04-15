import wave
import os
from pydub import AudioSegment
from steg_modules.crypto_utils import encrypt_message

def message_to_binary(message):
    return ''.join(format(ord(c), '08b') for c in message)

def encode_audio(input_audio, message, password=None):
    filename, ext = os.path.splitext(input_audio)

    # Convert .mp3 to .wav if needed
    if ext.lower() == '.mp3':
        print("Converting MP3 to WAV...")
        sound = AudioSegment.from_mp3(input_audio)
        input_audio = f"{filename}_converted.wav"
        sound.export(input_audio, format="wav")

    output_audio = f"{filename}_stego.wav"

    if password:
        message = encrypt_message(message, password)

    message += "<END>"
    binary_message = message_to_binary(message)
    binary_index = 0

    with wave.open(input_audio, 'rb') as audio:
        frames = bytearray(audio.readframes(audio.getnframes()))
        frame_count = len(frames)

        if len(binary_message) > frame_count:
            raise ValueError("Message too long to hide in audio!")

        for i in range(len(frames)):
            if binary_index < len(binary_message):
                frames[i] = (frames[i] & ~1) | int(binary_message[binary_index])
                binary_index += 1
            else:
                break

        with wave.open(output_audio, 'wb') as output:
            output.setparams(audio.getparams())
            output.writeframes(frames)

    print("Audio encoded and saved to:", output_audio)
    return output_audio
