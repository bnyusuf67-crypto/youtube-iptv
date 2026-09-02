import yt_dlp
import os

KANALLAR = {
    "TRT Haber": "@trthaber",
    "Halk TV": "@Halktvkanali",
    "Sözcü TV": "@sozcuTelevizyonu",
    "Habertürk": "@haberturktv"
}

def get_m3u8(channel_handle):
    url = f"https://youtube.com{channel_handle}/live"
    
    # İŞTE IP ENGELİNİ AŞAN FORMAT AYARLARI
    ydl_opts = {
        # 'best' yerine doğrudan '95' veya '96' gibi saf HLS format kodlarını zorluyoruz
        # Bu formatlar genellikle IP kilidine takılmadan dış oynatıcılarda (VLC vb.) çalışır
        'format': '95/96/bestvideo+bestaudio/best', 
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['web_embedded'], # Gömülü oynatıcı taklidi yaparak IP kilidini esnetir
            }
        }
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info.get('url')
        except:
            return None

# M3U Dosyasını Oluşturma
m3u_content = "#EXTM3U\n"
for kanal_adi, handle in KANALLAR.items():
    print(f"{kanal_adi} linki çözülüyor...")
    m3u8_url = get_m3u8(handle)
    if m3u8_url:
        m3u_content += f'#EXTINF:-1 tvg-name="{kanal_adi}",{kanal_adi}\n{m3u8_url}\n'

with open("liste.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)

print("liste.m3u başarıyla güncellendi!")
