from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd
from google.cloud import storage

app = Flask(__name__)

# 1. Extract: Mengambil data dari halaman web
def extract_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        books = soup.find_all('article', class_='product_pod')
        data = []
        for book in books:
            name = book.h3.a['title']
            price = book.find('p', class_='price_color').get_text(strip=True)
            rating = book.p['class'][1]
            data.append({'Name': name, 'Price': price, 'Rating': rating})
        return data
    else:
        print("Failed to retrieve data")
        return []

# 2. Transform: Membersihkan dan merapikan data
def transform_data(data):
    df = pd.DataFrame(data)
    df['Price'] = df['Price'].replace('[\£]', '', regex=True).astype(float)
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    df['Rating'] = df['Rating'].map(rating_map)
    return df

# 3. Load: Memuat data ke dalam file CSV dan meng-upload ke Google Cloud Storage
def load_data_and_upload(df, bucket_name, filename='books.csv'):
    local_file_path = filename
    df.to_csv(local_file_path, index=False)
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_filename(local_file_path)

# Endpoint untuk menjalankan ETL
@app.route('/run_etl', methods=['POST'])
def run_etl():
    url = 'http://books.toscrape.com/'
    bucket_name = 'suara-nusa-dev-labs-ml-test-1'
    data = extract_data(url)
    if not data:
        return jsonify({'message': 'No data extracted'}), 500
    df = transform_data(data)
    load_data_and_upload(df, bucket_name)
    return jsonify({'message': 'ETL process completed successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)