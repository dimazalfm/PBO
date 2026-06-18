class Produk:
    def __init__(self, kode: str, nama: str, stok: int, harga: float):
        self.kode = kode
        self.nama = nama
        self.stok = stok
        self.harga = harga

    def is_available(self) -> bool:
        return self.stok > 0

    def reduce_stok(self, jumlah: int) -> bool:
        if jumlah <= 0 or jumlah > self.stok:
            return False
        self.stok -= jumlah
        return True

    def tambah_stok(self, jumlah: int) -> None:
        if jumlah > 0:
            self.stok += jumlah

    def detail(self) -> str:
        return f"[{self.kode}] {self.nama} - Rp {self.harga:.0f} - Stok: {self.stok}"
