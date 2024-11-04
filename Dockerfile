# Gunakan image Python
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Salin requirements.txt dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin file utama
COPY main.py .

# Tetapkan FLASK_APP ke main.py
ENV FLASK_APP=main.py

# Jalankan aplikasi Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
