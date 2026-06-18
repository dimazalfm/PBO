from produk import Produk


class ItemTransaksi:
    def __init__(self, produk: Produk, jumlah: int):
        self.produk = produk
        self.jumlah = jumlah

    @property
    def subtotal(self) -> float:
        return self.produk.harga * self.jumlah

    def ringkasan(self) -> str:
        return f"{self.produk.nama} x{self.jumlah} = Rp {self.subtotal:.0f}"
