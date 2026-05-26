# 🪨 Aplikasi Analisis & Prediksi Batubara Indonesia

Aplikasi web interaktif ini dibangun menggunakan **Streamlit**, **Plotly**, dan **Pandas** untuk menganalisis tren kronologis serta memproyeksikan data batubara Indonesia beberapa tahun ke depan berdasarkan tren historis periode 2012–2024.

Aplikasi ini merupakan bagian dari Proyek Akhir Mata Kuliah Literasi Data dan Inteligensi Artifisial (WI2002) - Institut Teknologi Bandung (ITB) Tahun 2026.

## 👥 Kelompok 4 - Anggota Tim:
* Tyo Fazira Mukhtar / 12325072
* Bryan Derrian Jethro / 12325032
* Rainhard Marisi Sihombing / 12325034
* Hana Fayaza Hazimatul Khair / 12325046 
* Dipa Kalifa Ahmad / 12325040

## 📊 Variabel yang Dianalisis:
1. **Produksi Batubara Indonesia** (Juta Ton)
2. **Harga Batubara Global** (USD/Ton)
3. **Ekspor Batubara Indonesia** (Juta Ton)
4. **Konsumsi Domestik Indonesia** (Juta Ton)

## 🔮 Model Prediksi (Time Series Forecasting) yang Digunakan:
* **Garis Lurus (Linear Regression):** Mengasumsikan laju perkembangan data ke depan bersifat konstan dan stabil.
* **Lengkung (Polynomial Regression Derajat 2):** Menangkap pola percepatan atau perlambatan (akselerasi) dari tren masa lalu.
* **Momentum Terakhir (Holt's Double Exponential Smoothing):** Menghitung proyeksi dengan memberikan bobot evaluasi lebih tinggi pada tren data di tahun-tahun terakhir (2022–2024).

## 🛠️ Cara Menjalankan Secara Lokal (Mac/Windows):
1. Pastikan library yang dibutuhkan sudah terinstall:
   ```bash
   pip install streamlit numpy pandas plotly
