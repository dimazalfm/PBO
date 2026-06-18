import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional
from produk import Produk
from item_transaksi import ItemTransaksi
from transaksi import Transaksi
from kasir import Kasir
from datetime import datetime


class AplikasiKasirGUI:
    def __init__(self, master):
        self.master = master
        master.title("Aplikasi Kasir TokoClass")
        master.geometry("980x620")
        master.resizable(False, False)

        self.kasir = Kasir("admin", "Kasir Utama", "1234")
        self.katalog: List[Produk] = []
        self.transaksi: Optional[Transaksi] = None
        self.riwayat: List[Transaksi] = []

        self.inisialisasi_produk()
        self.build_login_frame()

    def inisialisasi_produk(self) -> None:
        self.katalog.extend([
            Produk("P001", "Pensil", 20, 3000),
            Produk("P002", "Buku Tulis", 50, 8500),
            Produk("P003", "Pulpen", 30, 5000),
            Produk("P004", "Penghapus", 25, 2500),
            Produk("P005", "Spidol", 15, 7000),
        ])

    def clear_frame(self) -> None:
        for widget in self.master.winfo_children():
            widget.destroy()

    def build_login_frame(self) -> None:
        self.clear_frame()
        frame = tk.Frame(self.master, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Login Kasir", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(frame, text="Username:").grid(row=1, column=0, sticky="e", pady=5)
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Password:").grid(row=2, column=0, sticky="e", pady=5)
        self.password_entry = tk.Entry(frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)

        login_button = tk.Button(frame, text="Masuk", width=20, command=self.login)
        login_button.grid(row=3, column=0, columnspan=2, pady=15)

        self.login_status = tk.Label(frame, text="", fg="red")
        self.login_status.grid(row=4, column=0, columnspan=2)

    def login(self) -> None:
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if self.kasir.username == username and self.kasir.login(password):
            self.build_main_menu()
        else:
            self.login_status.config(text="Username atau password salah.")

    def build_main_menu(self) -> None:
        self.clear_frame()
        top_frame = tk.Frame(self.master, padx=20, pady=15)
        top_frame.pack(fill="x")

        tk.Label(top_frame, text=f"Selamat datang, {self.kasir.nama}", font=("Arial", 16, "bold")).pack(side="left")
        logout_button = tk.Button(top_frame, text="Logout", command=self.build_login_frame)
        logout_button.pack(side="right")

        button_frame = tk.Frame(self.master, padx=20, pady=10)
        button_frame.pack(fill="x")

        tk.Button(button_frame, text="Cari Produk", width=18, command=self.build_search_frame).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Lihat Stok Produk", width=18, command=self.build_stock_frame).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Tambah Stok", width=18, command=self.build_add_stock_frame).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="Transaksi Baru", width=18, command=self.build_transaction_frame).grid(row=0, column=3, padx=5, pady=5)
        tk.Button(button_frame, text="Riwayat Transaksi", width=18, command=self.build_history_frame).grid(row=1, column=0, padx=5, pady=5)

        self.status_label = tk.Label(self.master, text="Pilih menu untuk memulai.", font=("Arial", 12))
        self.status_label.pack(padx=20, pady=10)

    def build_search_frame(self) -> None:
        self.clear_frame()
        header = tk.Frame(self.master, padx=20, pady=10)
        header.pack(fill="x")
        tk.Label(header, text="Cari Produk", font=("Arial", 16, "bold")).pack(side="left")
        tk.Button(header, text="Kembali", command=self.build_main_menu).pack(side="right")

        control_frame = tk.Frame(self.master, padx=20, pady=10)
        control_frame.pack(fill="x")
        tk.Label(control_frame, text="Masukkan nama atau kode:").grid(row=0, column=0, sticky="w")
        self.search_entry = tk.Entry(control_frame, width=40)
        self.search_entry.grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="Cari", command=self.search_products).grid(row=0, column=2, padx=5)

        self.search_result = tk.Listbox(self.master, width=90, height=15)
        self.search_result.pack(padx=20, pady=10)

    def search_products(self) -> None:
        keyword = self.search_entry.get().strip().lower()
        self.search_result.delete(0, tk.END)
        for produk in self.katalog:
            if keyword in produk.kode.lower() or keyword in produk.nama.lower():
                self.search_result.insert(tk.END, produk.detail())
        if self.search_result.size() == 0:
            self.search_result.insert(tk.END, "Produk tidak ditemukan.")

    def build_stock_frame(self) -> None:
        self.clear_frame()
        header = tk.Frame(self.master, padx=20, pady=10)
        header.pack(fill="x")
        tk.Label(header, text="Stok Produk", font=("Arial", 16, "bold")).pack(side="left")
        tk.Button(header, text="Kembali", command=self.build_main_menu).pack(side="right")

        columns = ("kode", "nama", "harga", "stok")
        tree = ttk.Treeview(self.master, columns=columns, show="headings", height=18)
        tree.heading("kode", text="Kode")
        tree.heading("nama", text="Nama Produk")
        tree.heading("harga", text="Harga")
        tree.heading("stok", text="Stok")
        tree.column("kode", width=100)
        tree.column("nama", width=380)
        tree.column("harga", width=120)
        tree.column("stok", width=80)
        tree.pack(padx=20, pady=10, fill="x")

        for produk in self.katalog:
            tree.insert("", tk.END, values=(produk.kode, produk.nama, f"Rp {produk.harga:.0f}", produk.stok))

    def build_add_stock_frame(self) -> None:
        self.clear_frame()
        header = tk.Frame(self.master, padx=20, pady=10)
        header.pack(fill="x")
        tk.Label(header, text="Tambah Stok / Produk Baru", font=("Arial", 16, "bold")).pack(side="left")
        tk.Button(header, text="Kembali", command=self.build_main_menu).pack(side="right")

        columns = ("kode", "nama", "harga", "stok")
        self.stock_tree = ttk.Treeview(self.master, columns=columns, show="headings", height=10)
        self.stock_tree.heading("kode", text="Kode")
        self.stock_tree.heading("nama", text="Nama Produk")
        self.stock_tree.heading("harga", text="Harga")
        self.stock_tree.heading("stok", text="Stok")
        self.stock_tree.column("kode", width=100)
        self.stock_tree.column("nama", width=380)
        self.stock_tree.column("harga", width=120)
        self.stock_tree.column("stok", width=80)
        self.stock_tree.pack(padx=20, pady=10, fill="x")

        self.refresh_stock_tree()

        form_frame = tk.Frame(self.master, padx=20, pady=5)
        form_frame.pack(fill="x")

        existing_frame = tk.LabelFrame(form_frame, text="Tambah Stok Produk Lama", padx=10, pady=8)
        existing_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        tk.Label(existing_frame, text="Jumlah stok tambahan:").grid(row=0, column=0, sticky="w", padx=5)
        self.add_stock_entry = tk.Entry(existing_frame, width=15)
        self.add_stock_entry.grid(row=0, column=1, padx=5)
        tk.Button(existing_frame, text="Tambah Stok", command=self.process_add_stock).grid(row=0, column=2, padx=5)

        new_frame = tk.LabelFrame(form_frame, text="Tambah Produk Baru", padx=10, pady=8)
        new_frame.grid(row=0, column=1, sticky="nsew")

        tk.Label(new_frame, text="Kode:").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.new_kode_entry = tk.Entry(new_frame, width=12)
        self.new_kode_entry.grid(row=0, column=1, padx=5, pady=3)

        tk.Label(new_frame, text="Nama:").grid(row=0, column=2, sticky="w", padx=5, pady=3)
        self.new_nama_entry = tk.Entry(new_frame, width=20)
        self.new_nama_entry.grid(row=0, column=3, padx=5, pady=3)

        tk.Label(new_frame, text="Harga:").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.new_harga_entry = tk.Entry(new_frame, width=12)
        self.new_harga_entry.grid(row=1, column=1, padx=5, pady=3)

        tk.Label(new_frame, text="Stok awal:").grid(row=1, column=2, sticky="w", padx=5, pady=3)
        self.new_stok_entry = tk.Entry(new_frame, width=12)
        self.new_stok_entry.grid(row=1, column=3, padx=5, pady=3)

        tk.Button(new_frame, text="Tambah Produk Baru", command=self.process_add_new_product).grid(
            row=2, column=0, columnspan=4, pady=8
        )

        self.add_stock_status = tk.Label(
            self.master,
            text="Pilih produk lama untuk menambah stok, atau isi form untuk menambah produk baru.",
            font=("Arial", 11),
        )
        self.add_stock_status.pack(padx=20, pady=5)

    def refresh_stock_tree(self) -> None:
        for row in self.stock_tree.get_children():
            self.stock_tree.delete(row)
        for produk in self.katalog:
            self.stock_tree.insert("", tk.END, values=(produk.kode, produk.nama, f"Rp {produk.harga:.0f}", produk.stok))

    def process_add_stock(self) -> None:
        selected = self.stock_tree.selection()
        if not selected:
            messagebox.showwarning("Perhatian", "Pilih produk terlebih dahulu.")
            return

        try:
            jumlah = int(self.add_stock_entry.get().strip())
        except ValueError:
            messagebox.showwarning("Perhatian", "Jumlah harus berupa angka.")
            return

        if jumlah <= 0:
            messagebox.showwarning("Perhatian", "Jumlah stok harus lebih besar dari 0.")
            return

        item = self.stock_tree.item(selected[0])
        kode = item["values"][0]
        produk = self.cari_produk_by_kode(kode)
        if produk is None:
            messagebox.showerror("Error", "Produk tidak ditemukan.")
            return

        stok_lama = produk.stok
        produk.tambah_stok(jumlah)

        self.refresh_stock_tree()
        self.add_stock_entry.delete(0, tk.END)
        self.add_stock_status.config(
            text=f"Stok {produk.nama} berhasil ditambah: {stok_lama} → {produk.stok} (+{jumlah})",
            fg="darkgreen",
        )
        messagebox.showinfo("Sukses", f"Stok {produk.nama} ditambah {jumlah} unit.\nStok sekarang: {produk.stok}")

    def process_add_new_product(self) -> None:
        kode = self.new_kode_entry.get().strip()
        nama = self.new_nama_entry.get().strip()
        harga_str = self.new_harga_entry.get().strip()
        stok_str = self.new_stok_entry.get().strip()

        if not kode or not nama:
            messagebox.showwarning("Perhatian", "Kode dan nama produk wajib diisi.")
            return

        if self.cari_produk_by_kode(kode) is not None:
            messagebox.showwarning("Perhatian", f"Kode produk '{kode}' sudah digunakan.")
            return

        try:
            harga = float(harga_str)
            stok = int(stok_str)
        except ValueError:
            messagebox.showwarning("Perhatian", "Harga dan stok harus berupa angka.")
            return

        if harga <= 0:
            messagebox.showwarning("Perhatian", "Harga harus lebih besar dari 0.")
            return

        if stok <= 0:
            messagebox.showwarning("Perhatian", "Stok awal harus lebih besar dari 0.")
            return

        produk_baru = Produk(kode, nama, stok, harga)
        self.katalog.append(produk_baru)
        self.refresh_stock_tree()

        self.new_kode_entry.delete(0, tk.END)
        self.new_nama_entry.delete(0, tk.END)
        self.new_harga_entry.delete(0, tk.END)
        self.new_stok_entry.delete(0, tk.END)

        self.add_stock_status.config(
            text=f"Produk baru ditambahkan: [{kode}] {nama} - Rp {harga:.0f} - Stok: {stok}",
            fg="darkgreen",
        )
        messagebox.showinfo(
            "Sukses",
            f"Produk baru berhasil ditambahkan.\n[{kode}] {nama}\nHarga: Rp {harga:.0f}\nStok awal: {stok}",
        )

    def build_transaction_frame(self) -> None:
        self.clear_frame()
        header = tk.Frame(self.master, padx=20, pady=10)
        header.pack(fill="x")
        tk.Label(header, text="Transaksi Baru", font=("Arial", 16, "bold")).pack(side="left")
        tk.Button(header, text="Kembali", command=self.build_main_menu).pack(side="right")

        self.transaksi = Transaksi(f"TRX{int(datetime.now().timestamp() * 1000)}")
        self.discount_value = 0.0

        main_frame = tk.Frame(self.master, padx=20, pady=10)
        main_frame.pack(fill="both", expand=False)

        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        product_frame = tk.LabelFrame(left_frame, text="Produk")
        product_frame.pack()

        columns = ("kode", "nama", "harga", "stok")
        self.product_tree = ttk.Treeview(product_frame, columns=columns, show="headings", height=8)
        for col, width in zip(columns, (80, 180, 80, 60)):
            self.product_tree.heading(col, text=col.capitalize())
            self.product_tree.column(col, width=width)
        self.product_tree.pack(side="left", fill="y")

        scrollbar = ttk.Scrollbar(product_frame, orient="vertical", command=self.product_tree.yview)
        self.product_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        for produk in self.katalog:
            self.product_tree.insert("", tk.END, values=(produk.kode, produk.nama, f"Rp {produk.harga:.0f}", produk.stok))

        action_frame = tk.Frame(left_frame)
        action_frame.pack(pady=10)

        tk.Label(action_frame, text="Jumlah:").pack(side="left", padx=5)
        self.quantity_entry = tk.Entry(action_frame, width=8)
        self.quantity_entry.pack(side="left", padx=5)
        tk.Button(action_frame, text="Tambah ke Keranjang", command=self.add_to_cart).pack(side="left", padx=5)

        cart_frame = tk.LabelFrame(left_frame, text="Keranjang")
        cart_frame.pack(pady=10)

        columns = ("nama", "jumlah", "subtotal")
        self.cart_tree = ttk.Treeview(cart_frame, columns=columns, show="headings", height=6)
        self.cart_tree.heading("nama", text="Nama Produk")
        self.cart_tree.heading("jumlah", text="Jumlah")
        self.cart_tree.heading("subtotal", text="Subtotal")
        self.cart_tree.column("nama", width=240)
        self.cart_tree.column("jumlah", width=60)
        self.cart_tree.column("subtotal", width=100)
        self.cart_tree.pack(fill="x", padx=5, pady=5)

        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        calc_frame = tk.LabelFrame(right_frame, text="Pembayaran", font=("Arial", 10, "bold"))
        calc_frame.pack(pady=10)

        tk.Label(calc_frame, text="Diskon (%):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.diskon_entry = tk.Entry(calc_frame, width=10)
        self.diskon_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(calc_frame, text="Terapkan", command=self.apply_discount).grid(row=0, column=2, padx=5, pady=5)

        self.total_label = tk.Label(calc_frame, text="Total: Rp 0", font=("Arial", 11, "bold"), fg="blue")
        self.total_label.grid(row=1, column=0, columnspan=3, pady=10, sticky="w", padx=5)

        tk.Label(calc_frame, text="Nominal Bayar:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.bayar_entry = tk.Entry(calc_frame, width=15)
        self.bayar_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        tk.Button(calc_frame, text="SUBMIT PEMBAYARAN", command=self.process_payment, bg="green", fg="white", font=("Arial", 10, "bold")).grid(row=3, column=0, columnspan=3, pady=10, padx=5, sticky="ew")

        self.change_label = tk.Label(calc_frame, text="Kembalian: Rp 0", font=("Arial", 11, "bold"), fg="darkgreen")
        self.change_label.grid(row=4, column=0, columnspan=3, pady=10, sticky="w", padx=5)

        receipt_frame = tk.LabelFrame(right_frame, text="Struk", font=("Arial", 10, "bold"))
        receipt_frame.pack(pady=10)

        self.receipt_text = tk.Text(receipt_frame, height=12, width=40, state="disabled")
        self.receipt_text.pack(fill="both", padx=5, pady=5)

        button_frame = tk.Frame(receipt_frame)
        button_frame.pack(pady=5)
        tk.Button(button_frame, text="Cetak Struk", command=self.show_receipt).pack()

    def add_to_cart(self) -> None:
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showwarning("Perhatian", "Pilih produk terlebih dahulu.")
            return

        try:
            jumlah = int(self.quantity_entry.get().strip())
        except ValueError:
            messagebox.showwarning("Perhatian", "Jumlah harus berupa angka.")
            return

        item = self.product_tree.item(selected[0])
        kode = item["values"][0]
        produk = self.cari_produk_by_kode(kode)
        if produk is None:
            messagebox.showerror("Error", "Produk tidak ditemukan.")
            return

        if jumlah <= 0 or not produk.reduce_stok(jumlah):
            messagebox.showwarning("Perhatian", "Stok tidak cukup atau jumlah tidak valid.")
            return

        self.transaksi.tambah_item(ItemTransaksi(produk, jumlah))
        self.cart_tree.insert("", tk.END, values=(produk.nama, jumlah, f"Rp {produk.harga * jumlah:.0f}"))
        self.quantity_entry.delete(0, tk.END)
        self.update_product_list()
        self.update_total_label()

    def update_product_list(self) -> None:
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        for produk in self.katalog:
            self.product_tree.insert("", tk.END, values=(produk.kode, produk.nama, f"Rp {produk.harga:.0f}", produk.stok))

    def apply_discount(self) -> None:
        if self.transaksi is None:
            return
        try:
            diskon = float(self.diskon_entry.get().strip())
        except ValueError:
            messagebox.showwarning("Perhatian", "Masukkan diskon dalam format angka.")
            return
        total = self.transaksi.terapkan_diskon(diskon)
        self.total_label.config(text=f"Total setelah diskon: Rp {total:.0f}")

    def process_payment(self) -> None:
        if self.transaksi is None:
            return
        try:
            bayar = float(self.bayar_entry.get().strip())
        except ValueError:
            messagebox.showwarning("Perhatian", "Masukkan nominal bayar yang valid.")
            return

        if not self.transaksi.proses_pembayaran(bayar):
            messagebox.showwarning("Perhatian", "Pembayaran gagal. Pastikan nominal cukup.")
            return

        kembalian = self.transaksi.hitung_kembalian()
        self.change_label.config(text=f"Kembalian: Rp {kembalian:.0f}")
        self.show_receipt()
        self.riwayat.append(self.transaksi)
        messagebox.showinfo("Sukses", "Pembayaran berhasil. Struk dicetak di layar.")

    def show_receipt(self) -> None:
        if self.transaksi is None:
            return
        struk = self.transaksi.cetak_struk()
        self.receipt_text.config(state="normal")
        self.receipt_text.delete("1.0", tk.END)
        self.receipt_text.insert(tk.END, struk)
        self.receipt_text.config(state="disabled")

    def build_history_frame(self) -> None:
        self.clear_frame()
        header = tk.Frame(self.master, padx=20, pady=10)
        header.pack(fill="x")
        tk.Label(header, text="Riwayat Transaksi", font=("Arial", 16, "bold")).pack(side="left")
        tk.Button(header, text="Kembali", command=self.build_main_menu).pack(side="right")

        self.history_tree = ttk.Treeview(self.master, columns=("id", "total", "status"), show="headings", height=18)
        self.history_tree.heading("id", text="ID Transaksi")
        self.history_tree.heading("total", text="Total")
        self.history_tree.heading("status", text="Status")
        self.history_tree.column("id", width=200)
        self.history_tree.column("total", width=140)
        self.history_tree.column("status", width=100)
        self.history_tree.pack(padx=20, pady=10, fill="x")

        for trx in self.riwayat:
            self.history_tree.insert("", tk.END, values=(trx.id_transaksi, f"Rp {trx.total_setelah_diskon():.0f}", "Selesai"))

        tk.Button(self.master, text="Lihat Struk Terpilih", command=self.show_selected_receipt).pack(pady=5)
        self.history_receipt = tk.Text(self.master, height=10, state="disabled")
        self.history_receipt.pack(padx=20, pady=10, fill="both")

    def show_selected_receipt(self) -> None:
        selected = self.history_tree.selection()
        if not selected:
            messagebox.showwarning("Perhatian", "Pilih transaksi dari daftar.")
            return
        values = self.history_tree.item(selected[0])["values"]
        trx_id = values[0]
        transaksi = next((trx for trx in self.riwayat if trx.id_transaksi == trx_id), None)
        if transaksi is None:
            return
        self.history_receipt.config(state="normal")
        self.history_receipt.delete("1.0", tk.END)
        self.history_receipt.insert(tk.END, transaksi.cetak_struk())
        self.history_receipt.config(state="disabled")

    def cari_produk_by_kode(self, kode: str) -> Optional[Produk]:
        for produk in self.katalog:
            if produk.kode.lower() == kode.lower():
                return produk
        return None


if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiKasirGUI(root)
    root.mainloop()
