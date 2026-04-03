import streamlit as st
import streamlit.components.v1 as components
import random
import json
import os
import time

# Sayfa yapılandırması
st.set_page_config(page_title="WINGPROG", layout="wide",page_icon="🏆")

VERITABANI_DOSYASI = "kullanici_verileri.json"

# --- JSON Veritabanı Fonksiyonları ---
def verileri_oku():
    if os.path.exists(VERITABANI_DOSYASI):
        with open(VERITABANI_DOSYASI, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def verileri_kaydet(veriler):
    with open(VERITABANI_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(veriler, f, ensure_ascii=False, indent=4)

def kullanici_kaydet():
    # Mevcut session state verilerini JSON'a yazar
    kullanici = st.session_state.aktif_kullanici
    veriler = verileri_oku()
    veriler[kullanici] = {
        "toplam_xp": st.session_state.toplam_xp,
        "gunluk_gorevler": st.session_state.gunluk_gorevler
    }
    verileri_kaydet(veriler)

# --- Veri Havuzları ---
ana_dersler = [
    {"gorev": "📐 Matematik: Güncel konudan 40 soru çöz (Orta Seviye)", "xp": 160},
    {"gorev": "📐 Matematik: Üçgenler yeni nesil 30 soru çöz (Zor Seviye)", "xp": 240},
    {"gorev": "📐 Matematik: Eski konulardan 50 soru ile genel tekrar yap (Kolay Seviye)", "xp": 100},
    {"gorev": "⚛️ Fizik: 20 dk tekrar yap (20XP) ve 20 soru çöz (Zor Seviye: 8x20)", "xp": 180},
    {"gorev": "⚛️ Fizik: 45 dk konu çalış (45XP) ve 20 soru çöz (Orta Seviye: 4x20)", "xp": 125},
    {"gorev": "🧪 Kimya: Konu özeti çıkar (30XP) ve 40 soru bitir (Kolay Seviye: 2x40)", "xp": 110},
    {"gorev": "🧪 Kimya: Madde ünitesinden 25 soru çöz (Zor Seviye)", "xp": 200},
    {"gorev": "🧬 Biyoloji: Son işlenen konudan 30 soru çöz (Orta Seviye)", "xp": 120},
    {"gorev": "🧬 Biyoloji: 20 dk not çıkar (20XP) ve 40 soru çöz (Orta Seviye: 4x40)", "xp": 180}
]

sozel_videolar = [
    {"gorev": "📜 Tarih: Güncel üniteden 30 dakika konu anlatımı izle", "xp": 30},
    {"gorev": "📜 Tarih: İlk Türk İslam Devletleri belgeseli/detaylı videosu izle (45 dk)", "xp": 45},
    {"gorev": "🌍 Coğrafya: 40 dakika konu anlatımı izle ve not al", "xp": 40},
    {"gorev": "🌍 Coğrafya: 20 dakika video izle ve 10 dakika dilsiz harita çalışması yap", "xp": 30},
    {"gorev": "✒️ Edebiyat: Eser/Yazar videolarından 25 dakika izle", "xp": 25},
    {"gorev": "✒️ Edebiyat: 40 dakika dil bilgisi konu anlatımı izle", "xp": 40}
]

yan_dersler = [
    {"gorev": "🇪🇳 İngilizce: 20 dakika kelime tekrarı ve cümle kurma", "xp": 20},
    {"gorev": "🇪🇳 İngilizce: 30 dakika okuma (reading) ve çeviri pratiği yap", "xp": 30},
    {"gorev": "🇪🇳 İngilizce: Gramer konusundan 40 soru çöz (Orta Seviye)", "xp": 160},
    {"gorev": "🕋 Din Kültürü: İlgili üniteden 20 soru çöz (Orta Seviye)", "xp": 80},
    {"gorev": "🕋 Din Kültürü: 15 dakika ünite özeti oku", "xp": 15},
    {"gorev": "🇩🇪 Almanca: 20 dakika yeni kelime ezberi yap", "xp": 25},
    {"gorev": "🇩🇪 Almanca: 30 dakika kelime tekrarı yap", "xp": 35},
    {"gorev": "🏥 Sağlık Bilgisi: Derste tutulan notları 15 dakika tekrar et", "xp": 15}
]

kitap_okuma = [
    {"gorev": "📚 20 dakika boyunca odaklanarak kitap oku", "xp": 20},
    {"gorev": "📚 30 dakika boyunca kitap oku", "xp": 30},
    {"gorev": "📚 45 dakika boyunca kitap oku", "xp": 45},
]

market_urunleri = [
    {"ad": "☕ 10 Dakika Kısa Mola", "fiyat": 25},
    {"ad": "🎵 Müzik Dinleyerek Uzanma (20 Dk)", "fiyat": 40},
    {"ad": "🥨 Kahve / Çay / Atıştırmalık", "fiyat": 50},
    {"ad": "📱 30 Dakika Sosyal Medya", "fiyat": 200},
    {"ad": "📺 1 Bölüm Dizi İzle", "fiyat": 150},
    {"ad": "🎮 1 Saat Oyun", "fiyat": 300},
    {"ad": "🎬 İstediğin Bir Filmi İzle", "fiyat": 500}
]

spor = [
    {"gorev":"🏀 30dk Spor","xp":30},
    {"gorev":"🏀 10dk Spor","xp":10},
    {"gorev":"🏀 20dk Spor","xp":20}
]

# --- Giriş Sistemi ---
if "aktif_kullanici" not in st.session_state:
    st.title("Kullanıcı Girişi")
    kullanici_adi = st.text_input("Kullanıcı Adınızı Girin:")
    
    if st.button("Giriş Yap / Kayıt Ol"):
        if kullanici_adi.strip() != "":
            st.session_state.aktif_kullanici = kullanici_adi.strip()
            
            # Veritabanını kontrol et
            veriler = verileri_oku()
            if st.session_state.aktif_kullanici in veriler:
                # Eski kullanıcı, verileri yükle
                kullanici_verisi = veriler[st.session_state.aktif_kullanici]
                st.session_state.toplam_xp = kullanici_verisi.get("toplam_xp", 0)
                st.session_state.gunluk_gorevler = kullanici_verisi.get("gunluk_gorevler", [])
            else:
                # Yeni kullanıcı, sıfırdan başlat
                st.session_state.toplam_xp = 0
                st.session_state.gunluk_gorevler = []
                kullanici_kaydet()
            
            st.rerun()
        else:
            st.error("Lütfen geçerli bir kullanıcı adı girin.")

# --- Ana Uygulama (Sadece giriş yapıldıysa çalışır) ---
else:
    # Yan Menü (Market ve Mevcut XP)
    st.sidebar.title(f"👤 Profil: {st.session_state.aktif_kullanici}")
    st.sidebar.metric("✨ Mevcut XP", f"{st.session_state.toplam_xp} XP")
    
    if st.sidebar.button("Çıkış Yap"):
        del st.session_state["aktif_kullanici"]
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.subheader("⏱️ Zamanlayıcı")
    
    timer_secenek = st.sidebar.selectbox("Süre Seçin", ["30 Dakika", "60 Dakika", "Özel"])
    
    if timer_secenek == "30 Dakika":
        sure_dk = 30
    elif timer_secenek == "60 Dakika":
        sure_dk = 60
    else:
        sure_dk = st.sidebar.number_input("Dakika Girin:", min_value=1, value=15)

    if st.sidebar.button("Zamanlayıcıyı Başlat"):
        sure_saniye = sure_dk * 60
        timer_alani = st.sidebar.empty() # Canlı güncelleme için boş alan
        
        while sure_saniye > 0:
            dakika, saniye = divmod(sure_saniye, 60)
            timer_alani.metric("Kalan Süre", f"{dakika:02d}:{saniye:02d}")
            time.sleep(1)
            sure_saniye -= 1
        
        timer_alani.success("Süre Doldu!")
        st.toast(f"Bildirim: {sure_dk} dakikalık çalışma süren bitti!", icon="🔔")
        st.balloons()
        components.html(
            f"""
            <script>
                alert("🔔 Bildirim: {sure_dk} dakikalık çalışma süren bitti!");
            </script>
            """,
            height=0, # Görünür bir alan kaplamaması için yüksekliği 0 yapabilirsin
        )

    st.sidebar.markdown("---")
    st.sidebar.subheader("Ödül Marketi")

    for urun in market_urunleri:
        col_ad, col_buton = st.sidebar.columns([2, 1])
        col_ad.write(f"{urun['ad']} ({urun['fiyat']} XP)")
        if col_buton.button("Al", key=f"market_{urun['ad']}"):
            if st.session_state.toplam_xp >= urun['fiyat']:
                st.session_state.toplam_xp -= urun['fiyat']
                kullanici_kaydet() # JSON'u güncelle
                st.sidebar.success(f"{urun['ad']} alındı!")
                st.rerun()
            else:
                st.sidebar.error("Yetersiz XP!")

    # Ana Sayfa
    st.title("WINGPROG v1.0")

    @st.dialog("Onay Gerekiyor")
    def onayi_goster():
        st.write("Yeni bir program oluşturulacak. Mevcut görevlerin silinebilir. Emin misin?")
        
        # Kullanıcı "Evet" butonuna basarsa işlemler burada gerçekleşir
        if st.button("Evet, Devam Et"):
            st.session_state.gunluk_gorevler = [
                random.choice(ana_dersler),
                random.choice(sozel_videolar),
                random.choice(yan_dersler),
                random.choice(kitap_okuma),
                random.choice(spor)
            ]
            kullanici_kaydet() # Yeni görevleri JSON'a kaydet
            st.success("Yeni program oluşturuldu!")
            st.rerun() # Diyaloğu kapatıp ana sayfayı güncellemek için şart

    # 2. Ana Buton
    if st.button("Yeni Program Oluştur"):
        onayi_goster()

    # 3. Görevleri Görüntüleme (Burası diyalog dışında, ana ekranda kalmalı)
    if st.session_state.gunluk_gorevler:
        st.subheader("Günün Görevleri")
        
        # Döngü içinde pop işlemi yaparken liste sırası bozulmaması için 
        # reversed (sondan başa) veya farklı bir yöntem kullanmak daha güvenlidir,
        # ama senin mantığında her seferinde st.rerun() olduğu için bu şekilde de çalışır.
        for i, gorev_verisi in enumerate(st.session_state.gunluk_gorevler):
            c1, c2 = st.columns([3, 1])
            c1.write(f"{i+1}- {gorev_verisi['gorev']} (+{gorev_verisi['xp']} XP)")
            
            if c2.button("Tamamladım", key=f"btn_{i}_{gorev_verisi['xp']}"):
                st.session_state.toplam_xp += gorev_verisi['xp']
                st.session_state.gunluk_gorevler.pop(i)
                kullanici_kaydet() 
                st.rerun()
    else:
        st.info("Henüz bir program oluşturulmadı. Yukarıdaki butona basarak başlayabilirsin.")