from transaksi import Transaksi


class Kasir:
    def __init__(self, username: str, nama: str, password: str):
        self.username = username
        self.nama = nama
        self._password = password
        self.riwayat_transaksi: list[Transaksi] = []

    def login(self, password_input: str) -> bool:
        return self._password == password_input

    def tambah_riwayat(self, transaksi: Transaksi) -> None:
        if transaksi and transaksi.selesai():
            self.riwayat_transaksi.append(transaksi)

    def get_riwayat(self) -> list[Transaksi]:
        return list(self.riwayat_transaksi)
