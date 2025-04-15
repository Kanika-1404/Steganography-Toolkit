from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
from PIL import Image
from pydub import AudioSegment

from steg_modules.image_steg import encoder as img_enc, decoder as img_dec
from steg_modules.audio_steg import encoder as aud_enc, decoder as aud_dec
from steg_modules.video_steg import encoder as vid_enc, decoder as vid_dec

port = int(os.environ.get("PORT", 5000))  # Use platform PORT or fallback to 5000

app.run(host="0.0.0.0", port=port)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def convert_to_png(filepath):
    if filepath.lower().endswith(('.jpg', '.jpeg')):
        img = Image.open(filepath)
        new_path = filepath.rsplit('.', 1)[0] + '.png'
        img.save(new_path)
        return new_path
    return filepath


def convert_mp3_to_wav(filepath):
    if filepath.lower().endswith('.mp3'):
        sound = AudioSegment.from_mp3(filepath)
        new_path = filepath.rsplit('.', 1)[0] + '.wav'
        sound.export(new_path, format="wav")
        return new_path
    return filepath


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/encode', methods=['GET', 'POST'])
def encode():
    if request.method == 'POST':
        filetype = request.form['filetype']
        message = request.form['message']
        password = request.form.get('password', '')
        file = request.files['file']

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Convert if needed
        if filetype == 'image':
            filepath = convert_to_png(filepath)
            output_path = img_enc.encode_image(filepath, message, None, password)
        elif filetype == 'audio':
            filepath = convert_mp3_to_wav(filepath)
            output_path = aud_enc.encode_audio(filepath, message, password)
        elif filetype == 'video':
            output_path = vid_enc.encode_video(filepath, message, password)
            return send_file(output_path, as_attachment=True, download_name="stego_video.avi", mimetype="video/x-msvideo")

        else:
            return "Unsupported file type", 400

        return send_file(output_path, as_attachment=True)

    return render_template('encode.html')


@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST':
        filetype = request.form['filetype']
        password = request.form.get('password', '')
        file = request.files['file']

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Convert if needed
        if filetype == 'image':
            filepath = convert_to_png(filepath)
            message = img_dec.decode_image(filepath, password)
        elif filetype == 'audio':
            filepath = convert_mp3_to_wav(filepath)
            message = aud_dec.decode_audio(filepath, password)
        elif filetype == 'video':
            message = vid_dec.decode_video(filepath, password)
        else:
            return "Unsupported file type", 400

        return render_template('result.html', message=message)

    return render_template('decode.html')



# Do nothing - Gunicorn will start it on render
# if __name__ == '__main__':
#     app.run(debug=True)
