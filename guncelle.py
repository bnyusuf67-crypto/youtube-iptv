import yt_dlp

# Nokta atışı canlı yayın URL'lerini doğrudan veriyoruz
KANALLAR = {
    "TRT Haber": "https://www.youtube.com/@trthaber/live",
    "Bizimev TV": "https://www.youtube.com/@bizimevtv2000/live",
    "Sözcü TV": "https://www.youtube.com/watch?v=ztmY_cCtUl0",
    "Diyanet Çocuk": "https://m.youtube.com/watch?v=_VsMIRdOtXI&pp=uAQw0gcJCSUBLa19xc3H"
}

def get_m3u8(live_url):
    ydl_opts = {
        'format': '95/96/bestvideo+bestaudio/best', 
        'quiet': True,
        'no_warnings': True,
        # Sadece YouTube ekstraktörünü zorla, harici DNS aramalarını/web sayfalarını engelle
        'allowed_extractors': ['youtube', 'youtube:live'], 
        'extractor_args': {
            'youtube': {
                'player_client': ['web_embedded'],
            }
        }
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(live_url, download=False)
            return info.get('url')
        except Exception as e:
            # Hatanın ne olduğunu tam görmek için yazdırıyoruz
            print(f"Bağlantı hatası: {e}")
            return None

# M3U Dosyasını Oluşturma
m3u_content = "#EXTM3U\n"
for kanal_adi, url in KANALLAR.items():
    print(f"{kanal_adi} linki çözülüyor...")
    m3u8_url = get_m3u8(url)
    if m3u8_url:
        m3u_content += f'#EXTINF:-1 tvg-name="{kanal_adi}",{kanal_adi}\n{m3u8_url}\n'

with open("liste.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)

print("liste.m3u başarıyla güncellendi!")
