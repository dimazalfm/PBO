from datetime import datetime
from item_transaksi import ItemTransaksi


class Transaksi:
    def __init__(self, id_transaksi: str):
        self.id_transaksi = id_transaksi
        self.waktu = datetime.now()
        self.item_list: list[ItemTransaksi] = []
        self.diskon_persen = 0.0
        self.jumlah_bayar = 0.0
        self.sudah_dibayar = False

    def tambah_item(self, item: ItemTransaksi) -> None:
        if item and item.jumlah > 0:
            self.item_list.append(item)

    def hitung_total(self) -> float:
        return sum(item.subtotal for item in self.item_list)

    def terapkan_diskon(self, persentase: float) -> float:
        if persentase <= 0 or persentase > 100 or not self.item_list:
            self.diskon_persen = 0.0
            return self.hitung_total()
        self.diskon_persen = persentase
        return self.total_setelah_diskon()

    def total_setelah_diskon(self) -> float:
        return self.hitung_total() * (100 - self.diskon_persen) / 100.0

    def proses_pembayaran(self, bayar: float) -> bool:
        if bayar < self.total_setelah_diskon() or not self.item_list:
            return False
        self.jumlah_bayar = bayar
        self.sudah_dibayar = True
        return True

    def hitung_kembalian(self) -> float:
        if not self.sudah_dibayar:
            return 0.0
        return self.jumlah_bayar - self.total_setelah_diskon()

    def cetak_struk(self) -> str:
        if not self.sudah_dibayar:
            return "Transaksi belum dibayar."

        lines = [
            "===== STRUK TRANSAKSI =====",
            f"ID: {self.id_transaksi}",
            f"Waktu: {self.waktu.strftime('%d/%m/%Y %H:%M:%S')}",
            "--------------------------"
        ]
        lines.extend(item.ringkasan() for item in self.item_list)
        lines.append("--------------------------")
        lines.append(f"Total: Rp {self.hitung_total():.0f}")
        if self.diskon_persen > 0:
            lines.append(f"Diskon: {self.diskon_persen:.0f}%")
            lines.append(f"Total setelah diskon: Rp {self.total_setelah_diskon():.0f}")
        lines.append(f"Bayar: Rp {self.jumlah_bayar:.0f}")
        lines.append(f"Kembalian: Rp {self.hitung_kembalian():.0f}")
        lines.append("==========================")
        return "\n".join(lines)

    def selesai(self) -> bool:
        return self.sudah_dibayar

    def ringkasan(self) -> str:
        return f"{self.id_transaksi} - Rp {self.total_setelah_diskon():.0f} - Dibayar: {'Ya' if self.sudah_dibayar else 'Belum'}"
