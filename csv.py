import pandas as pd

# Veri setinin dosya adı
DATASET_FILE = 'daily_news_titles.csv'

# Kategoriler ve örnek başlıklar ile URL'ler
data = {
    'title': [
        # Siyaset
        'Cumhurbaşkanı Erdoğan’ın Yeni Ekonomik Paket Açıklaması', 
        'Türkiye-AB İlişkilerinde Son Durum', 
        'Yerel Seçimlerde Sonuçlar ve Analizler', 
        'Meclis’te Yeni Yasalar Görüşülüyor', 
        'Siyasi Partilerden Seçim Stratejileri',

        # Sağlık
        'Covid-19’a Karşı Yeni Aşı Onaylandı', 
        'Türkiye’de Sağlık Reformları ve Etkileri', 
        'Sağlıkta Dijitalleşme: Yeni Uygulamalar', 
        'Büyük Hastanelerde Randevu Sorunları', 
        'Aşı Olmayanlara Yeni Kısıtlamalar',

        # Eğitim
        'Yeni Eğitim Yılı İçin Ders Programları Açıklandı', 
        'Uzaktan Eğitimde Başarı Oranları', 
        'Öğrenci Kayıtları İçin Son Tarih', 
        'Öğretmen Atamaları ve Eğitimde Değişiklikler', 
        'Eğitimde Teknoloji Kullanımı Artıyor',

        # Ekonomi
        'Döviz Kurları ve Ekonomik Tahminler', 
        'Enflasyon Raporu ve Etkileri', 
        'Borsa ve Finans Piyasalarındaki Son Gelişmeler', 
        'Türkiye Ekonomisinde Büyüme Rakamları', 
        'Yeni Yatırım Projeleri ve Ekonomik Etkileri'
    ],
    'url': [
        # Siyaset
        'https://www.trthaber.com/haber/turkiye/cumhurbaskani-erdogan-yeni-ekonomik-paket-aciklamasi-123456.html', 
        'https://www.trthaber.com/haber/turkiye/turkiye-ab-iliskilerinde-son-durum-123456.html', 
        'https://www.trthaber.com/haber/turkiye/yerel-secimlerde-sonuclar-ve-analizler-123456.html', 
        'https://www.trthaber.com/haber/turkiye/mecliste-yeni-yasalar-gorusuluyor-123456.html', 
        'https://www.trthaber.com/haber/turkiye/siyasi-partilerden-secim-stratejileri-123456.html',

        # Sağlık
        'https://www.trthaber.com/haber/saglik/covid-19a-karsi-yeni-asi-onaylandi-123456.html', 
        'https://www.trthaber.com/haber/saglik/turkiyede-saglik-reformlari-ve-etkileri-123456.html', 
        'https://www.trthaber.com/haber/saglik/saglikta-dijitallesme-yeni-uygulamalar-123456.html', 
        'https://www.trthaber.com/haber/saglik/buyuk-hastanelerde-randevu-sorunlari-123456.html', 
        'https://www.trthaber.com/haber/saglik/asi-olmayanlara-yeni-kisitlamalar-123456.html',

        # Eğitim
        'https://www.trthaber.com/haber/egitim/yeni-egitim-yili-icin-ders-programlari-aciklandi-123456.html', 
        'https://www.trthaber.com/haber/egitim/uzaktan-egitimde-basari-oranlari-123456.html', 
        'https://www.trthaber.com/haber/egitim/ogrenci-kayitlari-icin-son-tarih-123456.html', 
        'https://www.trthaber.com/haber/egitim/ogretmen-atamalari-ve-egitimde-degisiklikler-123456.html', 
        'https://www.trthaber.com/haber/egitim/egitimde-teknoloji-kullanimi-artiyor-123456.html',

        # Ekonomi
        'https://www.trthaber.com/haber/ekonomi/doviz-kurlari-ve-ekonomik-tahminler-123456.html', 
        'https://www.trthaber.com/haber/ekonomi/enflasyon-raporu-ve-etkileri-123456.html', 
        'https://www.trthaber.com/haber/ekonomi/borsa-ve-finans-piyasalarindaki-son-gelismeler-123456.html', 
        'https://www.trthaber.com/haber/ekonomi/turkiye-ekonomisinde-buyume-rakamlari-123456.html', 
        'https://www.trthaber.com/haber/ekonomi/yeni-yatirim-projeleri-ve-ekonomik-etkileri-123456.html'
    ]
}

# DataFrame oluşturun
df = pd.DataFrame(data)

# CSV dosyasına kaydedin
df.to_csv(DATASET_FILE, index=False)

print(f"Veri seti '{DATASET_FILE}' dosyasına kaydedildi.")

# Eksik verileri temizleme
df_cleaned = df.dropna()

# Temizlenmiş veriyi tekrar CSV dosyasına kaydet
df_cleaned.to_csv(DATASET_FILE, index=False)

print(f"Eksik veriler temizlendi ve '{DATASET_FILE}' dosyasına kaydedildi.")
