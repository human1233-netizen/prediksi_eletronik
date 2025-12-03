import streamlit as st
import pickle
import numpy as np

# ================================
# Simulasi Akun Login
# ================================
USER_CREDENTIALS = {
    "admin": "12345",
    "user": "password"
}

# State login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "menu" not in st.session_state:
    st.session_state.menu = "Dashboard"


# ================================
# Fungsi Login
# ================================
def login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.success("Login berhasil! Silakan lanjut ke dashboard.")
            st.experimental_rerun()
        else:
            st.error("Username atau password salah!")


# ================================
# Halaman: Informasi Perusahaan
# ================================
def informasi_perusahaan():
    st.title("Informasi Perusahaan")
    st.write("""
    **Nama Perusahaan:** PT Elektronik Widya Sejahtera  
    **Bidang:** Elektronik  
    **Deskripsi:** PT Elektronik Widya Sejahtera merupakan Perseroan Terbatas di Indonesia.
    """)
    st.markdown("---")
    # Tidak menggunakan st.info() untuk mencegah error


# ================================
# Halaman: Kontak
# ================================
def kontak():
    st.title("Kontak Kami")
    st.write("""
    **Alamat:** Jl. Total Jaya No. 16, Kel. Priuk, Tangerang  
    **Email:** electronic.widya@co.id  
    **Nomor Telepon:** 021-012235  
    """)
    st.markdown("---")
    # Tidak menggunakan st.info() untuk mencegah error


# ================================
# Halaman: Galeri
# ================================
def galeri():
    st.title("Galeri")
    st.write("Upload foto atau tampilkan gambar kegiatan perusahaan.")

    upload = st.file_uploader("Upload gambar", type=["jpg", "png", "jpeg"])
    if upload:
        st.image(upload, caption="Gambar yang diupload", use_column_width=True)


# ================================
# Halaman: Dashboard Prediksi
# ================================
def dashboard_prediksi():
    # Load model
    try:
        with open('model_rf_terbaik.pkl', 'rb') as f:
            model = pickle.load(f)
    except FileNotFoundError:
        st.error("Model tidak ditemukan: 'model_rf_terbaik.pkl'. Pastikan file ada di folder yang sama.")
        return
    except Exception as e:
        st.error(f"Terjadi error saat memuat model: {e}")
        return

    st.title("Prediksi Lama Produksi Alat Elektronik Impor")
    st.write("Gunakan aplikasi ini untuk memprediksi waktu produksi berdasarkan beberapa faktor.")

    jenis_produk = st.selectbox("Jenis Produk", ["AC", "Kulkas", "Televisi"])
    jenis_produk_encoded = {"AC": 0, "Kulkas": 1, "Televisi": 2}[jenis_produk]

    permintaan = st.number_input("Permintaan (unit)", min_value=0, step=1)
    stok_bahan = st.number_input("Stok Bahan (unit)", min_value=0, step=1)
    mesin_aktif = st.number_input("Jumlah Mesin Aktif", min_value=0, step=1)
    tenaga_kerja = st.number_input("Jumlah Tenaga Kerja", min_value=0, step=1)

    if st.button("Prediksi Lama Produksi"):
        try:
            input_data = np.array([[jenis_produk_encoded, permintaan, stok_bahan, mesin_aktif, tenaga_kerja]])
            prediksi = model.predict(input_data)
            st.success(f"Perkiraan Lama Produksi: **{prediksi[0]:.2f} jam**")
        except Exception as e:
            st.error(f"Gagal memprediksi: {e}")


# ================================
# Navigasi Menu Utama
# ================================
def main_menu():
    st.sidebar.title("Menu Utama")
    menu = st.sidebar.radio(
        "Pilih Halaman",
        ["Dashboard Prediksi", "Informasi Perusahaan", "Kontak", "Galeri", "Logout"]
    )

    if menu == "Dashboard Prediksi":
        dashboard_prediksi()
    elif menu == "Informasi Perusahaan":
        informasi_perusahaan()
    elif menu == "Kontak":
        kontak()
    elif menu == "Galeri":
        galeri()
    elif menu == "Logout":
        st.session_state.logged_in = False
        st.experimental_rerun()


# ================================
# MAIN
# ================================
if not st.session_state.logged_in:
    login()
else:
    main_menu()
