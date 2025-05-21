# transcriber.py
import io
from pydub import AudioSegment
from google.cloud import speech

def transcribe_audio(file_path):
    # Convert ogg to flac using pydub
    audio = AudioSegment.from_file(file_path, format="ogg")
    flac_io = io.BytesIO()
    audio.export(flac_io, format="flac")
    flac_io.seek(0)

    # Google Speech Recognition
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=flac_io.read())
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=48000,
        language_code="te-IN"
    )

    response = client.recognize(config=config, audio=audio)
    transcript = response.results[0].alternatives[0].transcript if response.results else ''
    return transcript
