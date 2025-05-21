from flask import Flask, request, jsonify
import os
import tempfile
import requests
import io
from pydub import AudioSegment
from google.cloud import speech

app = Flask(__name__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/etc/secrets/google-credentials.json"

def transcribe_ogg_bytes(ogg_bytes):
    # Convert OGG to FLAC
    audio = AudioSegment.from_file(io.BytesIO(ogg_bytes), format="ogg")
    flac_io = io.BytesIO()
    audio.export(flac_io, format="flac")
    flac_io.seek(0)

    # Transcribe using Google STT
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=flac_io.read())
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code="te-IN"
    )

    response = client.recognize(config=config, audio=audio)
    transcript = response.results[0].alternatives[0].transcript if response.results else ''
    return transcript

@app.route('/transcribe-audio', methods=['POST'])
def transcribe_audio():
    try:
        if 'url' in request.args:
            # ✅ WhatsApp audio URL (Botpress)
            url = request.args.get('url')
            token = os.environ.get("WHATSAPP_API_TOKEN")
            headers = {"Authorization": f"Bearer {token}"}
            res = requests.get(url, headers=headers)
            if res.status_code != 200:
                return jsonify({"error": "Failed to download audio"}), 400
            ogg_bytes = res.content

        elif 'audio' in request.files:
            # ✅ Manual audio upload (curl/file)
            ogg_bytes = request.files['audio'].read()

        else:
            return jsonify({'error': 'No audio file or URL provided'}), 400

        transcript = transcribe_ogg_bytes(ogg_bytes)
        return jsonify({'transcript': transcript})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
