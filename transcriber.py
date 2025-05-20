from flask import Flask, request, jsonify
import requests
from pydub import AudioSegment
import io
import os
from google.cloud import speech

app = Flask(__name__)

@app.route('/transcribe-audio', methods=['POST'])
def transcribe_audio():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No audio URL provided'}), 400

    # WhatsApp API token
    token = os.environ.get('WHATSAPP_API_TOKEN')
    headers = {"Authorization": f"Bearer {token}"}

    try:
        audio_response = requests.get(url, headers=headers)
        if audio_response.status_code != 200:
            return jsonify({'error': 'Failed to download audio'}), 400

        # Convert OGG to FLAC
        audio = AudioSegment.from_file(io.BytesIO(audio_response.content), format="ogg")
        flac_io = io.BytesIO()
        audio.export(flac_io, format="flac")
        flac_io.seek(0)

        # Transcribe with Google STT
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(content=flac_io.read())
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=16000,
            language_code="te-IN"
        )

        response = client.recognize(config=config, audio=audio)
        transcript = response.results[0].alternatives[0].transcript if response.results else ''
        return jsonify({"transcript": transcript})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
