import subprocess
import json
import io
from google.cloud import speech_v1p1beta1 as speech

def get_sample_rate(file_path):
    cmd = [
        'ffprobe', '-v', 'error', '-select_streams', 'a:0',
        '-show_entries', 'stream=sample_rate',
        '-of', 'json', file_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    rate = json.loads(result.stdout)['streams'][0]['sample_rate']
    return int(rate)

def transcribe_audio(file_path):
    sample_rate = get_sample_rate(file_path)
    client = speech.SpeechClient()
    
    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        sample_rate_hertz=sample_rate,
        language_code="te-IN",
        audio_channel_count=1
    )

    response = client.recognize(config=config, audio=audio)
    
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript
