from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import pandas as pd
import os

app = Flask(__name__)

# Hugging Face Transformers ile özetleme pipeline'ı oluşturma
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Veri seti dosya yolu
DATASET_FILE = 'news_dataset.csv'

# TEKNOFEST ile ilgili haber URL'sini almak için özel bir fonksiyon
def fetch_teknofest_titles():
    url = "https://www.trthaber.com/haber/bilim-teknoloji/teknofest-turkce-dogal-dil-isleme-yarismasinin-final-sureci-basladi-872146.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []

    title_tag = soup.find('h1')
    title = title_tag.get_text() if title_tag else "Başlık bulunamadı"

    results.append({'title': title, 'url': url})

    return results

# Kategoriler ve siteler
categories = {
    'gundem': fetch_teknofest_titles,
    'saglik': lambda: [],  # Boş bir fonksiyon örneği
    'egitim': lambda: [],  # Boş bir fonksiyon örneği
    'ekonomi': lambda: []  # Boş bir fonksiyon örneği
}

# Başlıkları veri setine kaydetme
def save_titles_to_dataset(titles):
    df = pd.DataFrame(titles)
    if os.path.exists(DATASET_FILE):
        existing_df = pd.read_csv(DATASET_FILE)
        df = pd.concat([existing_df, df], ignore_index=True).drop_duplicates(subset=['title'])
    df.to_csv(DATASET_FILE, index=False)

# Başlıkları güncelleme
def update_titles(selected_category):
    all_titles = categories[selected_category]()
    save_titles_to_dataset(all_titles)

# Veri setinden başlıkları yükleme
def load_titles_from_dataset():
    if os.path.exists(DATASET_FILE):
        df = pd.read_csv(DATASET_FILE)
        return df['title'].tolist()
    return []

# Arama başlığını bulma
def search_title(query):
    if os.path.exists(DATASET_FILE):
        df = pd.read_csv(DATASET_FILE)
        result = df[df['title'].str.contains(query, case=False, na=False)]
        return result.to_dict('records')
    return []

# Haber içeriğini çekme ve özetleme
def scrape_news(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return "Başlık bulunamadı", "İçerik bulunamadı"
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title_tag = soup.find('h1')
    title = title_tag.get_text() if title_tag else "Başlık bulunamadı"
    
    content_tags = soup.find_all('p')
    content = ' '.join([p.get_text() for p in content_tags]) if content_tags else "İçerik bulunamadı"
    
    return title, content

# Metni parçalama
def chunk_text(text, chunk_size=512):
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

# Haber özetleme
def summarize_news(url):
    title, content = scrape_news(url)
    chunks = chunk_text(content)
    summary = " ".join([summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text'] for chunk in chunks])
    return {'title': title, 'summary': summary, 'url': url}

# HTML şablonu
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Haber Metni Özetleyici</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1 class="mt-5">Tekno Parıltı Haber Metni Özetleyici</h1>
        <form action="/search" method="post">
            <div class="form-group">
                <label for="category">Kategori:</label>
                <select class="form-control" id="category" name="category" required>
                    <option value="gundem" {% if selected_category == 'gundem' %}selected{% endif %}>Gündem</option>
                    <option value="saglik" {% if selected_category == 'saglik' %}selected{% endif %}>Sağlık</option>
                    <option value="egitim" {% if selected_category == 'egitim' %}selected{% endif %}>Eğitim</option>
                    <option value="ekonomi" {% if selected_category == 'ekonomi' %}selected{% endif %}>Ekonomi</option>
                </select>
            </div>
            <div class="form-group">
                <label for="query">Haber Başlığı:</label>
                <select class="form-control" id="query" name="query" required>
                    {% for title in titles %}
                        <option value="{{ title }}">{{ title }}</option>
                    {% endfor %}
                </select>
            </div>
            <button type="submit" class="btn btn-primary">Ara</button>
        </form>
        
        {% if summaries %}
            <div class="mt-4">
                <h2>Özetler</h2>
                <ul>
                    {% for summary in summaries %}
                        <li>
                            <a href="{{ summary.url }}" target="_blank">{{ summary.title }}</a>
                            <p><strong>Özet:</strong> {{ summary.summary }}</p>
                        </li>
                    {% endfor %}
                </ul>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    selected_category = request.args.get('category', 'gundem')
    update_titles(selected_category)
    titles = load_titles_from_dataset()
    return render_template_string(html_template, titles=titles, selected_category=selected_category)

@app.route('/search', methods=['POST'])
def search():
    selected_category = request.form['category']
    update_titles(selected_category)
    query = request.form['query']
    title_results = search_title(query)
    summaries = [summarize_news(result['url']) for result in title_results]
    return render_template_string(
        html_template,
        titles=load_titles_from_dataset(),
        summaries=summaries,
        selected_category=selected_category
    )

@app.route('/fetch_summary', methods=['GET'])
def fetch_summary():
    url = request.args.get('url')
    if not url:
        return "URL parametresi gereklidir", 400
    summary = summarize_news(url)
    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Haber Özet</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container">
                <h1 class="mt-5">Tekno Parıltı Haber Özeti</h1>
                <h2>{{ summary.title }}</h2>
                <p><strong>Özet:</strong></p>
                <p>{{ summary.summary }}</p>
                <a href="{{ summary.url }}" target="_blank" class="btn btn-primary">Haberi Görüntüle</a>
            </div>
        </body>
        </html>
        """,
        summary=summary 
    )

if __name__ == '__main__':
    app.run(debug=True)
