import streamlit as st
import streamlit.components.v1 as components
import random
import json
from datetime import datetime, timedelta
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
    kullanici = st.session_state.aktif_kullanici
    veriler = verileri_oku()
    veriler[kullanici] = {
        "toplam_xp": st.session_state.toplam_xp,
        "gunluk_gorevler": st.session_state.gunluk_gorevler,
        # Yeni eklenenler:
        "son_olusturma_zamani": st.session_state.son_olusturma_zamani,
        "bonus_alindi": st.session_state.bonus_alindi
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
            # Giriş sistemi içinde verileri yüklediğin kısım
            if st.session_state.aktif_kullanici in veriler:
                kullanici_verisi = veriler[st.session_state.aktif_kullanici]
                st.session_state.toplam_xp = kullanici_verisi.get("toplam_xp", 0)
                st.session_state.gunluk_gorevler = kullanici_verisi.get("gunluk_gorevler", [])
                # Yeni eklenenler:
                st.session_state.son_olusturma_zamani = kullanici_verisi.get("son_olusturma_zamani", None)
                st.session_state.bonus_alindi = kullanici_verisi.get("bonus_alindi", False)
            else:
                # Yeni kullanıcı için varsayılanlar
                st.session_state.toplam_xp = 0
                st.session_state.gunluk_gorevler = []
                st.session_state.son_olusturma_zamani = None
                st.session_state.bonus_alindi = False
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
    # Ana Sayfa
    st.title("WINGPROG v1.0")

    @st.dialog("Onay Gerekiyor")
    def onayi_goster():
        st.write("Yeni bir program oluşturulacak. Mevcut görevlerin silinebilir. Emin misin?")
        
        if st.button("Evet, Devam Et"):
            st.session_state.gunluk_gorevler = [
                random.choice(ana_dersler),
                random.choice(sozel_videolar),
                random.choice(yan_dersler),
                random.choice(kitap_okuma),
                random.choice(spor)
            ]
            # BURASI ÖNEMLİ: Yeni zamanı kaydet ve bonusu sıfırla
            st.session_state.son_olusturma_zamani = datetime.now().isoformat()
            st.session_state.bonus_alindi = False
            
            kullanici_kaydet() # Yeni verileri JSON'a kaydet
            st.success("Yeni program oluşturuldu!")
            st.rerun() 

    # 24 Saat Kontrolü
    simdi = datetime.now()
    bugun_17 = simdi.replace(hour=17, minute=0, second=0, microsecond=0)

    # Eğer şu an saat 17.00'den önceyse, "en son reset saati" dünkü 17.00'dir.
    # Eğer şu an saat 17.00'den sonraysa, "en son reset saati" bugünkü 17.00'dir.
    if simdi < bugun_17:
        son_reset_zamani = bugun_17 - timedelta(days=1)
    else:
        son_reset_zamani = bugun_17

    yeni_program_hakki = True
    kalan_sure_mesaji = ""

    if st.session_state.son_olusturma_zamani:
        son_zaman = datetime.fromisoformat(st.session_state.son_olusturma_zamani)
        
        # Eğer kullanıcı en son programını son reset saatinden sonra oluşturduysa, 
        # yani bugün hakkını kullandıysa:
        if son_zaman > son_reset_zamani:
            yeni_program_hakki = False
            
            # Bir sonraki reset saati (bugün 17:00 geçtiyse yarın 17:00, geçmediyse bugün 17:00)
            if simdi < bugun_17:
                hedef_zaman = bugun_17
            else:
                hedef_zaman = bugun_17 + timedelta(days=1)
            
            fark = hedef_zaman - simdi
            # Saniyeleri saate ve KALAN saniyelere ayırıyoruz
            saat, kalan_saniye = divmod(fark.seconds, 3600)
            # Kalan saniyeleri dakikaya çeviriyoruz
            dakika = kalan_saniye // 60
            kalan_sure_mesaji = f"{saat} saat {dakika} dakika"

    # --- Buton ve Uyarı Görüntüleme ---
    if yeni_program_hakki:
        if st.button("🚀 Günlük Programı Oluştur"):
            onayi_goster()
    else:
        st.warning(f"Bugünkü hakkını kullandın. Yeni program için {kalan_sure_mesaji} sonra (saat 17.00'de) gelmelisin.")

    # --- 150 XP OR MYSTERY GIFT ---
    st.markdown("---")
    st.subheader("🤔 Zor Karar: 40 XP mi, Gizemli Kutu mu?")
    st.write("Tebrikler! Özel bir seçim hakkı kazandın. Garanti 40 XP'yi alıp gidebilirsin veya şansını gizemli kutuda deneyebilirsin!")

    # Durum takibi için session_state
    if "secim_yapildi" not in st.session_state:
        st.session_state.secim_yapildi = False

    if not st.session_state.secim_yapildi:
        col1, col2 = st.columns(2)
        with col1:
            st.info("### 💰 40 XP")
            st.write("Risk yok, garanti kazanç!")
            if st.button("Garanti XP'yi Al"):
                st.session_state.toplam_xp += 40
                st.session_state.secim_yapildi = True
                kullanici_kaydet()
                st.success("Cüzdana 40 XP eklendi!")
                st.rerun()

        with col2:
            st.warning("### 🎁 Gizemli Kutu")
            st.write("İçinde 500 XP de olabilir, -50 XP de!")
            if st.button("Şansımı Deneyeceğim!"):
                kutu_havuzu = [
                    {"ad": "💎 EFSANEVİ: 500 XP!", "deger": 500, "ihtimal": 10},
                    {"ad": "🎉 Harika: 200 XP!", "deger": 200, "ihtimal": 30},
                    {"ad": "😐 Eh İşte: 50 XP!", "deger": 50, "ihtimal": 30},
                    {"ad": "💀 Eyvah: -75 XP!", "deger": -750, "ihtimal": 20},
                    {"ad": "🌈 ŞAKA GİBİ: 1 XP!", "deger": 1, "ihtimal": 10}
                ]
                
                secenekler = [o["ad"] for o in kutu_havuzu]
                agirliklar = [o["ihtimal"] for o in kutu_havuzu]
                kazanan = random.choices(secenekler, weights=agirliklar, k=1)[0]
                secilen_odul = next(o for o in kutu_havuzu if o["ad"] == kazanan)
                
                st.session_state.toplam_xp += secilen_odul["deger"]
                st.session_state.secim_yapildi = True
                kullanici_kaydet()
                
                # Sonucu göster
                if secilen_odul["deger"] >= 200:
                    st.balloons()
                    st.success(f"İNANILMAZ! {secilen_odul['ad']}")
                else:
                    st.error(f"Kutudan bu çıktı: {secilen_odul['ad']}")
                
                st.rerun()
    else:
        st.write("✨ Bugünkü seçimini yaptın. Yarın yeni bir fırsat için tekrar gel!")

    # 3. Görevleri Görüntüleme ve Bonus Sistemi
    if st.session_state.gunluk_gorevler:
        st.subheader("Günün Görevleri")
        
        for i, gorev_verisi in enumerate(st.session_state.gunluk_gorevler):
            c1, c2 = st.columns([3, 1])
            c1.write(f"{i+1}- {gorev_verisi['gorev']} (+{gorev_verisi['xp']} XP)")
            
            if c2.button("Tamamladım", key=f"btn_{i}_{gorev_verisi['xp']}"):
                st.session_state.toplam_xp += gorev_verisi['xp']
                st.session_state.gunluk_gorevler.pop(i)
                kullanici_kaydet() 
                st.rerun()
                
    elif st.session_state.son_olusturma_zamani:
        if not st.session_state.bonus_alindi:
            st.success("Tebrikler! Günlük tüm görevleri tamamladın.")
            if st.button("🎁 150 XP Günlük Bonusu Al"):
                st.session_state.toplam_xp += 150
                st.session_state.bonus_alindi = True
                kullanici_kaydet()
                st.balloons()
                st.rerun()
        else:
            st.info("Bugünkü görevlerini tamamladın ve bonusunu aldın! Yeni program için beklemen gerekiyor.")
            st.caption("made by: qwertz.1.")

    else:
        st.info("Henüz bir program oluşturulmadı. Yukarıdaki butona basarak başlayabilirsin.")
