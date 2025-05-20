# app.py
from flask import Flask, request, jsonify
from transcriber import transcribe_audio
import os

app = Flask(__name__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/etc/secrets/google-credentials.json"


@app.route('/transcribe-audio', methods=['POST'])
def transcribe_audio_route():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    
    # ✅ Save file locally as .flac
    save_path = 'temp_audio.flac'
    audio_file.save(save_path)

    try:
        # ✅ Call transcriber with correct path
        transcript = transcribe_audio(save_path)
        return jsonify({'transcript': transcript})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(save_path):
            os.remove(save_path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
