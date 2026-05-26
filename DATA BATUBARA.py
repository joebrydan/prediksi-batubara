import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ── 1. KONFIGURASI HALAMAN WEBSITE ───────────────────────────────────────────
st.set_page_config(page_title="Prediksi Batubara - Kelompok 4", layout="wide")

st.title("🪨 Aplikasi Analisis & Prediksi Batubara Indonesia")
st.markdown("### Referensi Utama: Laporan Proyek LiDIA Kelompok 4 (2012-2024)")
st.write("---")

# ── 2. DATA HISTORIS DARI LAPORAN KELOMPOK 4 ──────────────────────────────────
TAHUN = np.array([2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])

PRODUKSI = np.array([386.000, 474.371, 458.097, 461.566, 456.198, 461.248, 557.772, 616.160, 563.728, 613.990, 687.432, 775.182, 836.130])
HARGA    = np.array([98.86, 85.32, 70.94, 58.94, 65.65, 88.16, 107.25, 77.99, 60.22, 136.68, 357.84, 173.80, 135.72])
EKSPOR   = np.array([347.504, 381.384, 356.302, 328.387, 311.329, 319.098, 343.124, 374.935, 341.547, 360.115, 360.115, 379.705, 405.761])
KONSUMSI = np.array([53.018, 57.014, 45.120, 51.156, 53.357, 57.176, 61.558, 138.420, 132.000, 133.000, 193.000, 213.000, 233.000])

# ── 3. PANEL KONTROL KIRI (SIDEBAR) ──────────────────────────────────────────
st.sidebar.header("🎛️ Pengaturan Prediksi")
komponen_pilihan = st.sidebar.selectbox(
    "Pilih Data yang Mau Ditebak:",
    ["Produksi Batubara Indonesia", "Harga Batubara Global", "Ekspor Batubara Indonesia", "Konsumsi Domestik Indonesia"]
)
jangka_waktu = st.sidebar.slider("Mau tebak berapa tahun ke depan?", min_value=1, max_value=10, value=5)

if komponen_pilihan == "Produksi Batubara Indonesia":
    data_aktif, unit = PRODUKSI, "Juta Ton"
elif komponen_pilihan == "Harga Batubara Global":
    data_aktif, unit = HARGA, "USD/Ton"
elif komponen_pilihan == "Ekspor Batubara Indonesia":
    data_aktif, unit = EKSPOR, "Juta Ton"
else:
    data_aktif, unit = KONSUMSI, "Juta Ton"

tahun_target = np.array([int(TAHUN[-1]) + i for i in range(1, jangka_waktu + 1)])

# ── 4. MESIN HITUNG MODEL PREDIKSI ────────────────────────────────────────────
t_historis = TAHUN - TAHUN[0]
t_target = tahun_target - TAHUN[0]

# Model A: Garis Lurus (Linear)
koef_linear = np.polyfit(t_historis, data_aktif, 1)
pred_linear = np.polyval(koef_linear, t_target)

# Model B: Lengkung (Polinomial Derajat 2)
koef_poly = np.polyfit(t_historis, data_aktif, 2)
pred_poly = np.polyval(koef_poly, t_target)

# Model C: Momentum Terakhir (Holt DES)
def rumus_holt_des(y_hist, steps, alpha=0.4, beta=0.3):
    L, T = y_hist[0], y_hist[1] - y_hist[0]
    for i in range(1, len(y_hist)):
        L_lalu, T_lalu = L, T
        L = alpha * y_hist[i] + (1 - alpha) * (L_lalu + T_lalu)
        T = beta * (L - L_lalu) + (1 - beta) * T_lalu
    return [L + h * T for h in range(1, steps + 1)]

pred_holt = rumus_holt_des(data_aktif, jangka_waktu)

# ── 5. PEMBUATAN GRAFIK INTERAKTIF (PLOTLY) ───────────────────────────────────
fig = go.Figure()

fig.add_trace(go.Scatter(x=TAHUN, y=data_aktif, name="Data Historis Asli", mode="lines+markers", line=dict(color="black", width=3)))

titik_sambung = data_aktif[-1]
y_plot_linear = np.insert(pred_linear, 0, titik_sambung)
y_plot_poly = np.insert(pred_poly, 0, titik_sambung)
y_plot_holt = np.insert(pred_holt, 0, titik_sambung)
x_plot_prediksi = np.insert(tahun_target, 0, TAHUN[-1])

fig.add_trace(go.Scatter(x=x_plot_prediksi, y=y_plot_linear, name="Model Garis Lurus (Linear)", mode="lines+markers", line=dict(dash="dash", color="blue")))
fig.add_trace(go.Scatter(x=x_plot_prediksi, y=y_plot_poly, name="Model Lengkung (Poly 2)", mode="lines+markers", line=dict(dash="dash", color="green")))
fig.add_trace(go.Scatter(x=x_plot_prediksi, y=y_plot_holt, name="Model Momentum (Holt DES)", mode="lines+markers", line=dict(dash="dash", color="orange")))

fig.update_layout(
    title=f"Tren & Proyeksi Masa Depan - {komponen_pilihan}",
    xaxis_title="Tahun",
    yaxis_title=f"Nilai ({unit})",
    hovermode="x unified",
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)

st.plotly_chart(fig, use_container_width=True)

# ── 6. PENYAJIAN TABEL DATA YANG SUDAH DIPERBAIKI (BEBAS ERROR) ───────────────
kolom_kiri, kolom_kanan = st.columns([2, 1])

with kolom_kiri:
    st.subheader("📋 Angka Hasil Estimasi Proyeksi")
    
    # Format tabel menggunakan struktur Dictionary agar nama kolom terbaca otomatis
    data_tabel_bersih = {
        "Tahun": [int(thn) for thn in tahun_target],
        "Garis Lurus (Linear)": [f"{pred_linear[i]:.2f} {unit}" for i in range(len(tahun_target))],
        "Lengkung (Poly 2)": [f"{pred_poly[i]:.2f} {unit}" for i in range(len(tahun_target))],
        "Momentum (Holt DES)": [f"{pred_holt[i]:.2f} {unit}" for i in range(len(tahun_target))]
    }
    
    # Tampilkan ke web screen tanpa menggunakan argument 'columns'
    st.table(data_tabel_bersih)

with kolom_kanan:
    st.subheader("💡 Cara Membaca Model")
    st.info(
        "**1. Garis Lurus (Linear):** Mengasumsikan laju perkembangan data ke depan akan konstan dan stabil.\n\n"
        "**2. Lengkung (Poly 2):** Cocok untuk jangka pendek karena menangkap pola percepatan dari tren masa lalu.\n\n"
        "**3. Momentum (Holt DES):** Sangat direkomendasikan karena memberikan bobot evaluasi lebih tinggi pada data tahun-tahun terakhir."
    )