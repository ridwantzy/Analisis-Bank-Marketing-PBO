from dataclasses import dataclass
from abc import ABC

# ======================================================================
# PILAR OOP: ENKAPSULASI & HIERARKI CUSTOM EXCEPTION (Sesuai Standar Dosen)
# ======================================================================
class BankAnalysisError(Exception):
    """Base exception untuk semua error di sistem Bank Marketing."""
    pass

class NasabahTidakValid(BankAnalysisError):
    """Error jika data atribut nasabah melanggar aturan bisnis bank."""
    pass

class DatasetFormatError(BankAnalysisError):
    """Error jika terjadi kegagalan parsing format data pada file CSV."""
    pass

# ======================================================================
# SOLID: Single Responsibility Principle (Model murni untuk representasi data)
# ======================================================================
@dataclass
class BankCustomer:
    """Model data tunggal untuk merepresentasikan seorang nasabah bank."""
    customer_id: str
    age: int
    job: str
    balance: float
    housing: str
    y_target: str   

    def __post_init__(self):
        """
        Tukang Jaga/Validasi Data saat objek berhasil dibuat.
        Menerapkan prinsip fail-fast untuk menjaga integritas data memori.
        """
        if self.age < 0:
            raise NasabahTidakValid(f"Validasi Gagal: Usia tidak boleh negatif! (Input: {self.age})")
        if not self.customer_id.strip():
            raise NasabahTidakValid("Validasi Gagal: Customer ID tidak boleh kosong!")
        if self.y_target.lower() not in ("yes", "no"):
            raise NasabahTidakValid(f"Validasi Gagal: Target kelulusan 'y' harus 'yes' atau 'no'! (Input: {self.y_target})")

    # Helper method untuk meningkatkan keterbacaan kode (Readability)
    def is_subscribed(self) -> bool:
        return self.y_target.lower() == "yes"

    def has_housing_loan(self) -> bool:
        return self.housing.lower() == "yes"

    def __str__(self) -> str:
        status = "SUKSES" if self.is_subscribed() else "MENOLAK"
        return f"Nasabah {self.customer_id} | Umur: {self.age} | Saldo: ${self.balance:,} | Status: [{status}]"
    
