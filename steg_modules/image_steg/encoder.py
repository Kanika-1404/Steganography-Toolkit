from PIL import Image
import os
from steg_modules.crypto_utils import encrypt_message

def message_to_binary(message):
    return ''.join(format(ord(char), '08b') for char in message)

def encode_image(image_path, secret_message, output_path=None, password=None):
    if password:
        secret_message = encrypt_message(secret_message, password)

    secret_message += "<END>"  # Use a custom delimiter
    binary_message = message_to_binary(secret_message)
    binary_index = 0

    image = Image.open(image_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    pixels = list(image.getdata())
    new_pixels = []

    for pixel in pixels:
        if binary_index < len(binary_message):
            r, g, b = pixel
            r = (r & ~1) | int(binary_message[binary_index])
            binary_index += 1

            if binary_index < len(binary_message):
                g = (g & ~1) | int(binary_message[binary_index])
                binary_index += 1

            if binary_index < len(binary_message):
                b = (b & ~1) | int(binary_message[binary_index])
                binary_index += 1

            new_pixels.append((r, g, b))
        else:
            new_pixels.append(pixel)

    new_image = Image.new(image.mode, image.size)
    new_image.putdata(new_pixels)

    # Set default output path if not provided
    if not output_path:
        file_name = os.path.splitext(os.path.basename(image_path))[0]
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{file_name}_stego.png")  # Always use .png for safety

    # Force save as PNG
    new_image.save(output_path, format='PNG')
    print("Encoding complete! Saved to", output_path)

    return output_path
