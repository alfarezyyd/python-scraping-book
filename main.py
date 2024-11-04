import requests
from bs4 import BeautifulSoup
import pandas as pd
from google.cloud import storage

# 1. Extract: Mengambil data dari halaman web
def extract_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Temukan elemen yang mengandung data buku
        books = soup.find_all('article', class_='product_pod')
        
        # Simpan data ke list
        data = []
        for book in books:
            name = book.h3.a['title']
            price = book.find('p', class_='price_color').get_text(strip=True)
            rating = book.p['class'][1]  # Rating adalah kelas CSS ke-2
            
            data.append({
                'Name': name,
                'Price': price,
                'Rating': rating
            })
        return data
    else:
        print("Failed to retrieve data")
        return []

# 2. Transform: Membersihkan dan merapikan data
def transform_data(data):
    df = pd.DataFrame(data)
    
    # Membersihkan kolom harga
    df['Price'] = df['Price'].replace('[\£]', '', regex=True).astype(float)  # Menghapus simbol "£"
    
    # Mengonversi rating dari teks ke angka (optional)
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    df['Rating'] = df['Rating'].map(rating_map)
    
    return df

# 3. Load: Memuat data ke dalam file CSV dan meng-upload ke Google Cloud Storage
def load_data_and_upload(df, bucket_name, filename='books.csv'):
    # Menyimpan CSV secara lokal
    local_file_path = filename
    df.to_csv(local_file_path, index=False)
    print(f"Data saved locally as {local_file_path}")

    # Meng-upload ke Google Cloud Storage
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(filename)
    
    blob.upload_from_filename(local_file_path)
    print(f"Data uploaded to bucket {bucket_name} as {filename}")

# Main ETL function
def run_etl(url, bucket_name):
    print("Starting ETL process...")
    
    # Extract
    data = extract_data(url)
    print(f"Extracted {len(data)} records")
    
    # Transform
    df = transform_data(data)
    print("Data transformed")
    
    # Load and upload
    load_data_and_upload(df, bucket_name)
    print("ETL process completed")

# URL dari halaman Books to Scrape
url = 'http://books.toscrape.com/'

# Ganti dengan nama bucket Anda
bucket_name = 'suara-nusa-dev-labs-ml-test-1'  # Misalnya, 'my-bucket'
run_etl(url, bucket_name)
