import csv
import os
from models_01 import BankCustomer, DatasetFormatError

# ======================================================================
# SOLID: Interface Segregation & Single Responsibility Principle
# ======================================================================
class BankCustomerRepository:
    """Repository Pattern khusus mengurus pembacaan dataset bank-full.csv."""
    
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._customers: list[BankCustomer] = []  # Menyimpan koleksi objek nasabah

    def load_csv(self) -> int:
        """
        Membaca file CSV dengan delimiter ';' sesuai karakteristik dataset bank.
        Mengubah baris teks menjadi objek BankCustomer secara otomatis.
        """
        if not os.path.exists(self._file_path):
            raise FileNotFoundError(f"File data [{self._file_path}] tidak ditemukan!")

        # Reset penampung data jika fungsi dipanggil ulang
        self._customers.clear()

        try:
            with open(self._file_path, mode='r', encoding='utf-8') as f:
                # Menggunakan DictReader dengan pemisah titik koma (;) sesuai gaya data UCI
                reader = csv.DictReader(f, delimiter=';')
                
                for idx, row in enumerate(reader):
                    try:
                        customer = BankCustomer(
                            customer_id=f"CUST_{idx+1:05d}",
                            age=int(row['age']),
                            job=row['job'].strip(),
                            balance=float(row['balance']),
                            housing=row['housing'].strip(),
                            y_target=row['y'].strip()
                        )
                        self._customers.append(customer)
                    except (ValueError, KeyError) as e:
                        raise DatasetFormatError(f"Gagal memproses baris data ke-{idx+1}: Atribut rusak/cacat. Detail: {e}")
            
            return len(self._customers)
        except Exception as e:
            if not isinstance(e, DatasetFormatError):
                raise DatasetFormatError(f"Terjadi kesalahan fatal pada operasi pembacaan file: {e}")
            raise e

    def get_all(self) -> list[BankCustomer]:
        """Menyediakan akses publik aman ke seluruh koleksi objek nasabah."""
        return self._customers

    def filter_by_job(self, target_job: str) -> list[BankCustomer]:
        """Helper untuk menyaring data nasabah berdasarkan jenis pekerjaan."""
        return [c for c in self._customers if c.job.lower() == target_job.lower()]
