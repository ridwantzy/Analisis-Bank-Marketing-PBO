import sys
from repositories_02 import BankCustomerRepository
from services_03 import BankAnalysisService
from models_01 import BankAnalysisError

def cetak_pembatas():
    print("=" * 55)

def tampilkan_menu():
    cetak_pembatas()
    print("     BANK MARKETING CAMPAIGN ANALYSIS SYSTEM (OOP)")
    cetak_pembatas()
    print(" [1] Tampilkan Statistik Global Kampanye")
    print(" [2] Analisis Hubungan Saldo Rekening vs Konversi")
    print(" [3] Analisis Karakteristik Usia Nasabah")
    print(" [4] Analisis Efek Beban Cicilan Rumah (Housing Loan)")
    print(" [5] Analisis Berdasarkan Jenis Pekerjaan Nasabah")
    print(" [6] Jalankan Semua Analisis Sekaligus (Run All)")
    print(" [0] Keluar dari Sistem")
    cetak_pembatas()

def main():
    # Menentukan target file data
    TARGET_FILE = '/content/drive/MyDrive/UAS PBO/bank-full.csv'
    repo = BankCustomerRepository(TARGET_FILE)

    print("\n Menginisialisasi Sistem Informasi Perbankan...")
    
    # Kunci Pengaman Utama: Menerapkan blok try-except Custom Exception Dosen
    try:
        total_data = repo.load_csv()
        print(f"[✓] Sukses memuat dataset perbankan. Tersimpan {total_data:,} objek di memori.\n")
    except FileNotFoundError as e:
        print(f"[❌] Error Fatal: {e}")
        print("Harap pastikan file 'bank-full.csv' sudah diunggah di lokasi yang benar.")
        sys.exit(1)
    except BankAnalysisError as e:
        print(f"[❌] Kegagalan Integritas Objek: {e}")
        print("Aplikasi dimatikan otomatis untuk menghindari salah kalkulasi statistik.")
        sys.exit(1)

    # Memasukkan koleksi objek ke dalam gerbang Service Layer
    service = BankAnalysisService(repo.get_all())

    while True:
        tampilkan_menu()
        pilihan = input("Masukkan nomor menu analisis Anda (0-4): ").strip()

        if pilihan == "1":
            global_res = service.dapatkan_ringkasan_global()
            print("\n STATISTIK GLOBAL DATA KAMPANYE:")
            print(f" -> Total Basis Data Nasabah : {global_res['total_nasabah']:,} orang")
            print(f" -> Rasio Sukses Deposito     : {global_res['conversion_rate_global']:.2f}%")
            print("")

        elif pilihan == "2":
            res = service.eksekusi_analisis_saldo()
            print(f"\n {res['metrik'].upper()}:")
            print(f" -> Rerata Saldo Nasabah Sukses Deposito (Yes) : ${res['rata_rata_saldo_sukses']:,.2f}")
            print(f" -> Rerata Saldo Nasabah Menolak Deposito (No)  : ${res['rata_rata_saldo_menolak']:,.2f}")
            print("\n INTERPRETASI: Nasabah dengan kondisi finansial mapan (saldo lebih tinggi) memiliki kecenderungan lebih besar menerima tawaran deposito.")

        elif pilihan == "3":
            res = service.eksekusi_analisis_usia()
            print(f"\n👥 {res['metrik'].upper()}:")
            print(f" -> Kelompok Usia Muda (<40 Tahun)  : Total {res['muda_total']:,} orang | Rasio Sukses: {res['muda_rate']:.2f}%")
            print(f" -> Kelompok Usia Matang (>=40 Tahun): Total {res['matang_total']:,} orang | Rasio Sukses: {res['matang_rate']:.2f}%")
            print("\n INTERPRETASI: Perbedaan rasio konversi antar kelompok umur membantu tim telemarketing memetakan prioritas panggilan.")

        elif pilihan == "4":
            res = service.eksekusi_analisis_cicilan()
            print(f"\n {res['metrik'].upper()}:")
            print(f" -> Memiliki Pinjaman Cicilan Rumah : Total {res['cicilan_total']:,} orang | Rasio Sukses: {res['cicilan_rate']:.2f}%")
            print(f" -> Bebas Beban Cicilan Rumah       : Total {res['bebas_total']:,} orang | Rasio Sukses: {res['bebas_bebas_rate'] if 'bebas_bebas_rate' in res else res['bebas_rate']:.2f}%")
            print("\n INTERPRETASI: Nasabah yang bebas dari cicilan rumah memiliki alokasi dana menganggur (idle fund) lebih banyak untuk dijadikan deposito.")

        elif pilihan == "5":
            res = service.eksekusi_analisis_pekerjaan()
            print(f"\n {res['metrik'].upper()}:")
            for job_title, detail in res['data_pekerjaan'].items():
                print(f" -> Pekerjaan: {job_title:<13} | Total: {detail['total']:,} orang | Rasio Sukses: {detail['rate']:.2f}%")
            print()

        elif pilihan == "6":
            print("\n" + "="*55)
            print(" RUN ALL: MENJALANKAN SELURUH FITUR ANALISIS SISTEM")
            print("="*55)
            
            # 1. Statistik Global
            global_res = service.dapatkan_ringkasan_global()
            print("\n [1] STATISTIK GLOBAL DATA KAMPANYE:")
            print(f" -> Total Basis Data Nasabah : {global_res['total_nasabah']:,} orang")
            print(f" -> Rasio Konversi Global    : {global_res['conversion_rate_global']:.2f}%")
            
            # 2. Aspek Finansial
            res2 = service.eksekusi_analisis_saldo()
            print(f"\n [2] {res2['metrik'].upper()}:")
            print(f" -> Rerata Saldo Nasabah Sukses Deposito (Yes) : ${res2['rata_rata_saldo_sukses']:,.2f}")
            print(f" -> Rerata Saldo Nasabah Menolak Deposito (No)  : ${res2['rata_rata_saldo_menolak']:,.2f}")
            
            # 3. Demografi Usia
            res3 = service.eksekusi_analisis_usia()
            print(f"\n [3] {res3['metrik'].upper()}:")
            print(f" -> Kelompok Usia Muda   (< 40 Thn) | Total: {res3['muda_total']:,} orang | Rasio Sukses: {res3['muda_rate']:.2f}%")
            print(f" -> Kelompok Usia Matang (>= 40 Thn) | Total: {res3['matang_total']:,} orang | Rasio Sukses: {res3['matang_rate']:.2f}%")
            
            # 4. Aspek Kampanye / Cicilan
            res4 = service.eksekusi_analisis_cicilan()
            print(f"\n [4] {res4['metrik'].upper()}:")
            print(f" -> Bebas Cicilan Rumah (No Loan)   | Total: {res4['bebas_total']:,} orang | Rasio Sukses: {res4['bebas_rate']:.2f}%")
            print(f" -> Memiliki Cicilan Rumah (Loan)   | Total: {res4['cicilan_total']:,} orang | Rasio Sukses: {res4['cicilan_rate']:.2f}%")
            
            # 5. Status Kerja
            res5 = service.eksekusi_analisis_pekerjaan()
            print(f"\n [5] {res5['metrik'].upper()}:")
            for job_title, detail in res5['data_pekerjaan'].items():
                print(f" -> Pekerjaan: {job_title:<45} | Total: {detail['total']:,} orang | Rasio Sukses: {detail['rate']:.2f}%")
                
            print("\n" + "="*55)
            print("✓ Seluruh laporan analisis data berhasil dicetak seutuhnya!")
            print("="*55 + "\n")
          
        elif pilihan == "0":
            print("\n[✓] Menutup Sesi Aplikasi Analisis. Terima kasih")
            break
        else:
            print("\n Pilihan tidak terdaftar. Harap masukkan angka bulat dari range 0 sampai 4.")

if __name__ == "__main__":
    main()
