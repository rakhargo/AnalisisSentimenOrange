import pandas as pd
import re

# Membaca data dari file CSV
df = pd.read_csv('data_review.csv')
df

def clean_review(row): # bersihkan setiap row
    nama_pembeli = str(row['Nama pembeli']) if pd.notna(row['Nama pembeli']) else ''
    column4_text = str(row['Column 4'])
    tanggal_pembelian = str(row['Tanggal pembelian']) if pd.notna(row['Tanggal pembelian']) else ''

    if nama_pembeli:
        column4_text = column4_text.replace(nama_pembeli, "")
    
    if pd.isna(row['Nama pembeli']):
        column4_text = column4_text[7:]
    
    # Jika ada tanggal pembelian, hapus tanggal beserta teks sebelumnya
    if tanggal_pembelian:
        column4_text = column4_text.replace(tanggal_pembelian, "")

    # Hapus informasi metadata lainnya
    column4_text = re.sub(r'Laporkan Penyalahgunaan', '', column4_text, flags=re.IGNORECASE)
    column4_text = re.sub(r'Membantu\?', '', column4_text)
    column4_text = re.sub(r'\d$', '', column4_text)

    return column4_text

df['Review'] = df.apply(clean_review, axis=1)

rating_cycle = [5, 4, 3, 2, 1]
rating_length = len(rating_cycle)
ratings = []

for i in range(len(df)):
    ratings.append(rating_cycle[(i // 66) % rating_length]) # membuat rating manual, setiap 66 data

df['Rating'] = ratings
df['Sentimen'] = df['Rating'].apply(lambda x: 'Positif' if x > 3 else 'Negatif') # sentimen berdasarkan rating

df = df[df['Review'] != ''] # null

df = df.applymap(lambda x: x.replace('\n', ' ') if isinstance(x, str) else x) # newline

df.to_csv('cleaned_data_review.csv', index=False) # save