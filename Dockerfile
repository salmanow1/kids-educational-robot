FROM python:3.10-slim

# تثبيت أداة FFmpeg للمونتاج والدمج التلقائي للحروف والعلامة المائية
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
