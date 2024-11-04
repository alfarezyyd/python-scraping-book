# Menggunakan image Python 3.10 sebagai base image
FROM python:3.10-slim

# Set environment variable
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Menyalin file requirements.txt dan script ke dalam container
COPY requirements.txt .
COPY etl_script.py .

# Menginstal dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Perintah untuk menjalankan script
CMD ["python", "etl_script.py"]
