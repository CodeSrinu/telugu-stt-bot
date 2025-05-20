FROM python:3.10-slim

WORKDIR /app

# Install ffmpeg (for ffprobe)
RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY transcriber.py .
COPY creds/ creds/
COPY audio/ audio/

ENV GOOGLE_APPLICATION_CREDENTIALS=creds/credentials.json

CMD ["python", "app.py"]
