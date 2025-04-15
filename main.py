# from image_steg.encoder import encode_image
# from image_steg.decoder import decode_image

# # Encode
# encode_image("input.png", "Secret message with Password Protection!", "encoded.png", password="kanika123")

# # Decode
# decode_image("encoded.png", password="kanika123")







# from audio_steg.encoder import encode_audio
# from audio_steg.decoder import decode_audio

# # Encode
# encode_audio("input.wav", "This is a secret audio message 🎧", "encoded.wav", password="kanika123")

# # Decode
# decode_audio("encoded.wav", password="kanika123")






from video_steg.encoder import encode_video
from video_steg.decoder import decode_video

# Encode
encode_video("input_video.mp4", "Secret video message 🎬", "stego_video.avi", password="kanika123")

# Decode
decode_video("stego_video.avi", password="kanika123")
