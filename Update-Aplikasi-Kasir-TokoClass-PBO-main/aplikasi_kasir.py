from kasir import Kasir
from produk import Produk
from item_transaksi import ItemTransaksi
from transaksi import Transaksi
from datetime import datetime


class AplikasiKasir:
    def __init__(self):
        self.katalog: list[Produk] = []
        self.kasir = Kasir("admin", "Kasir Utama", "1234")
        self.inisialisasi_produk()

    def inisialisasi_produk(self) -> None:
        self.katalog.extend([
            Produk("P001", "Pensil", 20, 3000),
            Produk("P002", "Buku Tulis", 50, 8500),
            Produk("P003", "Pulpen", 30, 5000),
            Produk("P004", "Penghapus", 25, 2500),
            Produk("P005", "Spidol", 15, 7000),
        ])

    def jalankan(self) -> None:
        print("=== Aplikasi Kasir TokoClass ===")
        if not self.login_kasir():
            print("Login gagal. Program dihentikan.")
            return

        selesai = False
        while not selesai:
            self.tampilkan_menu()
            pilihan = self.baca_angka("Pilih menu: ")
            if pilihan == 1:
                self.cari_produk()
            elif pilihan == 2:
                self.lihat_stok()
            elif pilihan == 3:
                self.proses_transaksi()
            elif pilihan == 4:
                self.lihat_riwayat()
            elif pilihan == 5:
                self.tambah_stok_produk()
            elif pilihan == 6:
                selesai = True
                print("Terima kasih. Sampai jumpa!")
            else:
                print("Pilihan tidak valid.")

    def login_kasir(self) -> bool:
        print("Login Kasir")
        user = input("Username: ").strip()
        password = input("Password: ").strip()
        if self.kasir.username == user and self.kasir.login(password):
            print(f"Login berhasil. Selamat datang, {self.kasir.nama}!")
            return True
        return False

    def tampilkan_menu(self) -> None:
        print("\n--- Menu Utama ---")
        print("1. Cari Produk")
        print("2. Lihat Stok Produk")
        print("3. Mulai Transaksi Baru")
        print("4. Lihat Riwayat Transaksi")
        print("5. Tambah Stok Produk")
        print("6. Keluar")

    def cari_produk(self) -> None:
        kata_kunci = input("Masukkan nama atau kode produk: ").strip().lower()
        hasil = [produk for produk in self.katalog if kata_kunci in produk.nama.lower() or kata_kunci in produk.kode.lower()]
        if not hasil:
            print("Produk tidak ditemukan.")
            return
        print("Hasil pencarian:")
        for produk in hasil:
            print(produk.detail())

    def lihat_stok(self) -> None:
        print("Daftar stok produk:")
        for produk in self.katalog:
            print(produk.detail())

    def tambah_stok_produk(self) -> None:
        print("--- Tambah Stok / Produk Baru ---")
        print("1. Tambah stok produk lama")
        print("2. Tambah produk baru")
        pilihan = self.baca_angka("Pilih menu: ")
        if pilihan == 1:
            self.tambah_stok_produk_lama()
        elif pilihan == 2:
            self.tambah_produk_baru()
        else:
            print("Pilihan tidak valid.")

    def tambah_stok_produk_lama(self) -> None:
        kode = input("Masukkan kode produk: ").strip()
        produk = self.cari_produk_by_kode(kode)
        if produk is None:
            print("Produk tidak ditemukan.")
            return
        print(f"Produk: {produk.detail()}")
        jumlah = self.baca_angka("Jumlah stok yang ditambahkan: ")
        if jumlah <= 0:
            print("Jumlah stok harus lebih besar dari 0.")
            return
        stok_lama = produk.stok
        produk.tambah_stok(jumlah)
        print(f"Stok berhasil ditambah: {stok_lama} → {produk.stok} (+{jumlah})")

    def tambah_produk_baru(self) -> None:
        kode = input("Masukkan kode produk baru: ").strip()
        if not kode:
            print("Kode produk tidak boleh kosong.")
            return
        if self.cari_produk_by_kode(kode) is not None:
            print(f"Kode produk '{kode}' sudah digunakan.")
            return

        nama = input("Masukkan nama produk: ").strip()
        if not nama:
            print("Nama produk tidak boleh kosong.")
            return

        harga = self.baca_desimal("Masukkan harga produk: ")
        if harga <= 0:
            print("Harga harus lebih besar dari 0.")
            return

        stok = self.baca_angka("Masukkan stok awal: ")
        if stok <= 0:
            print("Stok awal harus lebih besar dari 0.")
            return

        produk_baru = Produk(kode, nama, stok, harga)
        self.katalog.append(produk_baru)
        print("Produk baru berhasil ditambahkan:")
        print(produk_baru.detail())

    def proses_transaksi(self) -> None:
        transaksi = Transaksi(f"TRX{int(datetime.now().timestamp() * 1000)}")
        print("--- Tambah Item Belanja ---")
        while True:
            kode = input("Masukkan kode produk (atau ketik selesai): ").strip()
            if kode.lower() == "selesai":
                break
            produk = self.cari_produk_by_kode(kode)
            if produk is None:
                print("Produk tidak ditemukan.")
                continue
            print(produk.detail())
            jumlah = self.baca_angka("Jumlah: ")
            if jumlah <= 0:
                print("Jumlah harus lebih besar dari 0.")
                continue
            if not produk.reduce_stok(jumlah):
                print("Stok tidak cukup atau jumlah invalid.")
                continue
            transaksi.tambah_item(ItemTransaksi(produk, jumlah))
            print("Item ditambahkan ke keranjang.")

        if transaksi.hitung_total() <= 0:
            print("Tidak ada item dalam transaksi.")
            return

        print("--- Hitung Total Belanja ---")
        print(f"Total sementara: Rp {transaksi.hitung_total():.0f}")
        jawaban = input("Apakah ingin terapkan diskon? (y/n): ").strip().lower()
        if jawaban == "y":
            diskon = self.baca_desimal("Masukkan persentase diskon (0-100): ")
            total_setelah_diskon = transaksi.terapkan_diskon(diskon)
            print(f"Total setelah diskon: Rp {total_setelah_diskon:.0f}")
        else:
            transaksi.terapkan_diskon(0)

        print("--- Proses Pembayaran ---")
        total_bayar = transaksi.total_setelah_diskon()
        while True:
            bayar = self.baca_desimal(f"Bayar (Rp {total_bayar:.0f}): ")
            if transaksi.proses_pembayaran(bayar):
                print("Pembayaran berhasil.")
                print(f"Kembalian: Rp {transaksi.hitung_kembalian():.0f}")
                break
            print("Pembayaran gagal. Masukkan nominal yang cukup.")

        print("--- Cetak Struk ---")
        print(transaksi.cetak_struk())
        self.kasir.tambah_riwayat(transaksi)

    def cari_produk_by_kode(self, kode: str):
        for produk in self.katalog:
            if produk.kode.lower() == kode.lower():
                return produk
        return None

    def lihat_riwayat(self) -> None:
        print("--- Riwayat Transaksi ---")
        riwayat = self.kasir.get_riwayat()
        if not riwayat:
            print("Belum ada transaksi selesai.")
            return
        for trx in riwayat:
            print(trx.ringkasan())

    def baca_angka(self, prompt: str) -> int:
        while True:
            try:
                return int(input(prompt).strip())
            except ValueError:
                print("Masukkan angka yang valid.")

    def baca_desimal(self, prompt: str) -> float:
        while True:
            try:
                return float(input(prompt).strip())
            except ValueError:
                print("Masukkan angka yang valid.")


if __name__ == "__main__":
    AplikasiKasir().jalankan()
