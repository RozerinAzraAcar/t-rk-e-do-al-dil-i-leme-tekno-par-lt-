import requests
from bs4 import BeautifulSoup
import pandas as pd

# TRT Haber'den başlıkları çekme
def fetch_trt_haber_titles(category):
    search_url = f"https://www.trthaber.com/{category}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []

    for link in soup.find_all('a', href=True):
        if '/haber/' in link['href']:
            full_url = f"https://www.trthaber.com{link['href']}"
            title = link.get_text(strip=True)
            if title:  # Boş başlıkları filtreleme
                results.append({'title': title, 'url': full_url})

    return results

# Kategoriler ve TRT Haber siteleri
categories = {
    'siyaset': 'siyaset',
    'saglik': 'saglik',
    'egitim': 'egitim',
    'ekonomi': 'ekonomi'
}

# Veri seti oluşturma
data = {'title': [], 'url': []}

# Verileri çekme
for category, site_category in categories.items():
    titles = fetch_trt_haber_titles(site_category)
    for item in titles:
        data['title'].append(item['title'])
        data['url'].append(item['url'])

# DataFrame oluşturma
df = pd.DataFrame(data)

# CSV dosyasını kaydetme
df.to_csv('news_dataset.csv', index=False)
print("Veri seti oluşturuldu ve 'news_dataset.csv' dosyasına kaydedildi.")
