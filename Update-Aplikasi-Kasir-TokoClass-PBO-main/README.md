# Aplikasi Kasir TokoClass

Aplikasi kasir sederhana berbasis Python sesuai use case:
- Login Kasir
- Cari Produk
- Lihat Stok Produk
- Tambah Produk
- Tambah Item Belanja
- Hitung Total Belanja
- Terapkan Diskon (opsional)
- Proses Pembayaran
- Hitung Kembalian
- Cetak Struk
- Lihat Riwayat Transaksi

## Struktur Kode
- `produk.py` — model data produk
- `item_transaksi.py` — item belanja dalam transaksi
- `transaksi.py` — alur transaksi dan pembayaran
- `kasir.py` — autentikasi dan riwayat transaksi
- `aplikasi_kasir.py` — entry point dan menu interaktif

## Cara menjalankan
1. Buka terminal di folder `d:\Kuliah\PBO-Aplikasi Kasir TokoClass`
2. Jalankan aplikasi GUI dengan `python aplikasi_kasir_gui.py`

## Paket Aplikasi untuk Laptop
- Untuk Windows, kamu bisa membuat file executable dengan `pyinstaller --onefile aplikasi_kasir_gui.py`
- `APK` adalah format Android, bukan laptop. Untuk laptop biasanya dibuat executable di Windows (`.exe`) atau paket desktop lain.

## Akun Kasir
- Username: `admin`
- Password: `1234`
