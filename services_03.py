from abc import ABC, abstractmethod
from models_01 import BankCustomer

# ======================================================================
# PILAR OOP: ABSTRAKSI & POLIMORFISME
# SOLID: Open-Closed Principle (Bebas menambah jenis analisis tanpa mengubah induk)
# ======================================================================
class BaseBankAnalyzer(ABC):
    """Abstract Base Class (ABC) sebagai cetakan wajib seluruh kelas analisis."""
    
    def __init__(self, data: list[BankCustomer]):
        self._data = data  # Di-enkapsulasi sebagai protected attribute

    @abstractmethod
    def analyze(self) -> dict:
        """Fungsi abstrak yang wajib diimplementasikan ulang oleh kelas anak."""
        pass

    def get_conversion_rate(self) -> float:
        """Fungsi pembantu global untuk menghitung rasio sukses (%) kampanye."""
        if not self._data:
            return 0.0
        success_count = sum(1 for c in self._data if c.is_subscribed())
        return (success_count / len(self._data)) * 100

# ======================================================================
# SUBCLASS 1: Analisis Finansial Nasabah 
# ======================================================================
class BalanceAnalyzer(BaseBankAnalyzer):
    """Menghitung perbandingan rata-rata saldo nasabah yang Setuju vs Menolak."""
    
    def analyze(self) -> dict:
        yes_group = [c for c in self._data if c.is_subscribed()]
        no_group = [c for c in self._data if not c.is_subscribed()]

        avg_yes = sum(c.balance for c in yes_group) / len(yes_group) if yes_group else 0.0
        avg_no = sum(c.balance for c in no_group) / len(no_group) if no_group else 0.0

        return {
            "metrik": "Analisis Saldo Rekening (Financial Aspect)",
            "rata_rata_saldo_sukses": avg_yes,
            "rata_rata_saldo_menolak": avg_no
        }

# ======================================================================
# SUBCLASS 2: Analisis Demografi Usia (Tugas Anggota Kelompok 4)
# ======================================================================
class DemographicAnalyzer(BaseBankAnalyzer):
    """Menghitung persentase keberhasilan marketing berdasarkan kelompok umur."""
    
    def analyze(self) -> dict:
        muda = [c for c in self._data if c.age < 40]
        matang = [c for c in self._data if c.age >= 40]

        sukses_muda = sum(1 for c in muda if c.is_subscribed())
        sukses_matang = sum(1 for c in matang if c.is_subscribed())

        return {
            "metrik": "Analisis Demografi Usia Nasabah",
            "muda_total": len(muda),
            "muda_rate": (sukses_muda / len(muda) * 100) if muda else 0.0,
            "matang_total": len(matang),
            "matang_rate": (sukses_matang / len(matang) * 100) if matang else 0.0
        }

# ======================================================================
# SUBCLASS 3: Analisis Aspek Kampanye/Kredit (Tugas Anggota Kelompok 5)
# ======================================================================
class CampaignAnalyzer(BaseBankAnalyzer):
    """Mengukur efek kepemilikan cicilan rumah (housing loan) terhadap konversi."""
    
    def analyze(self) -> dict:
        punya_cicilan = [c for c in self._data if c.has_housing_loan()]
        bebas_cicilan = [c for c in self._data if not c.has_housing_loan()]

        sukses_cicilan = sum(1 for c in punya_cicilan if c.is_subscribed())
        sukses_bebas = sum(1 for c in bebas_cicilan if c.is_subscribed())

        return {
            "metrik": "Analisis Dampak Beban Cicilan Rumah Nasabah",
            "cicilan_total": len(punya_cicilan),
            "cicilan_rate": (sukses_cicilan / len(punya_cicilan) * 100) if punya_cicilan else 0.0,
            "bebas_total": len(bebas_cicilan),
            "bebas_rate": (sukses_bebas / len(bebas_cicilan) * 100) if bebas_cicilan else 0.0
        }

# ======================================================================
# SUBCLASS 4: Analisis Berdasarkan Jenis Pekerjaan (Tugas Anggota Kelompok 6)
# ======================================================================
class JobAnalyzer(BaseBankAnalyzer):
    """Mengukur rasio kesuksesan kampanye berdasarkan status keaktifan kerja nasabah."""
    def analyze(self) -> dict:
        aktif_jobs = ["management", "admin.", "technician", "blue-collar", "services", "entrepreneur", "self-employed"]
        
        stats = {
            "Kelompok Aktif Bekerja": {"total": 0, "sukses": 0},
            "Kelompok Non-Aktif (Student/Retired/Unemployed)": {"total": 0, "sukses": 0}
        }
        
        for c in self._data:
            job_lower = c.job.lower()
            if job_lower in aktif_jobs:
                key = "Kelompok Aktif Bekerja"
            else:
                key = "Kelompok Non-Aktif (Student/Retired/Unemployed)"
                
            stats[key]["total"] += 1
            if c.is_subscribed():
                stats[key]["sukses"] += 1
                
        hasil_analisis = {}
        for kategori, data in stats.items():
            total = data["total"]
            sukses = data["sukses"]
            hasil_analisis[kategori] = {
                "total": total,
                "rate": (sukses / total * 100) if total else 0.0
            }
            
        return {
            "metrik": "Analisis Berdasarkan Status Keaktifan Kerja Nasabah",
            "data_pekerjaan": hasil_analisis
        }

# ======================================================================
# LAYER 4: SERVICE LAYER (Orkestrator Utama Proyek)
# SOLID: Dependency Inversion Principle (Mengorkestrasikan sub-layer analyzer)
# ======================================================================
class BankAnalysisService:
    """Manajer Pusat Aplikasi yang merajut kerja sama Repository dan Analyzer."""
    
    def __init__(self, raw_data: list[BankCustomer]):
        self._data = raw_data
        self._balance_analyzer = BalanceAnalyzer(raw_data)
        self._demographic_analyzer = DemographicAnalyzer(raw_data)
        self._campaign_analyzer = CampaignAnalyzer(raw_data)
        self._job_analyzer = JobAnalyzer(raw_data)

    def dapatkan_ringkasan_global(self) -> dict:
        return {
            "total_nasabah": len(self._data),
            "conversion_rate_global": self._balance_analyzer.get_conversion_rate()
        }

    def eksekusi_analisis_saldo(self) -> dict:
        return self._balance_analyzer.analyze()

    def eksekusi_analisis_usia(self) -> dict:
        return self._demographic_analyzer.analyze()

    def eksekusi_analisis_cicilan(self) -> dict:
        return self._campaign_analyzer.analyze()

    def eksekusi_analisis_pekerjaan(self) -> dict:
        return self._job_analyzer.analyze()
