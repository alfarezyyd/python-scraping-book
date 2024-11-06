# Gunakan image Python 3.9 sebagai base image
FROM python:3.9-slim

# Set working directory di dalam kontainer
WORKDIR /app

# Salin file requirements.txt dan install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh file proyek (termasuk skrip Python Anda)
COPY . .

# Jalankan skrip Python saat kontainer dijalankan
CMD ["python", "main.py"]
