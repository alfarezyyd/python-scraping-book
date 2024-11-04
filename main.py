import requests
from bs4 import BeautifulSoup
import pandas as pd

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

# 3. Load: Memuat data ke dalam file CSV
def load_data(df, filename='books.csv'):
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main ETL function
def run_etl(url):
    print("Starting ETL process...")
    
    # Extract
    data = extract_data(url)
    print(f"Extracted {len(data)} records")
    
    # Transform
    df = transform_data(data)
    print("Data transformed")
    
    # Load
    load_data(df)
    print("ETL process completed")

# URL dari halaman Books to Scrape
url = 'http://books.toscrape.com/'
run_etl(url)