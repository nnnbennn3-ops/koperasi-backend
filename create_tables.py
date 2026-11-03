import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.configs.database import Base, engine

# Import semua entities terbaru
from src.entities.master.UserBankMappingEntity import MtrUserBankMapping
from src.entities.master.SavingTypeEntity import MtrSavingType
from src.entities.master.FormEntity import MtrFormTemplate
from src.entities.transaction.SavingEntity import TrxSavingAccount, TrxSavingTransaction
from src.entities.transaction.LoanEntity import TrxLoan, TrxLoanInstallment


def main():
    print("Menghubungkan ke SQL Server 2022 (koperasi_karyawan)...")
    try:
        # Bersihkan tabel lama agar tidak bentrok dengan skema baru
        print("Membersihkan tabel lama...")
        Base.metadata.drop_all(bind=engine)

        # Buat seluruh tabel baru dari kode
        print("Membuat semua tabel baru dari kode...")
        Base.metadata.create_all(bind=engine)
        print("\n SUKSES! Seluruh tabel baru berhasil dibuat dari kode:")
        print("  - mtr_user_bank_mapping (1 user = 1 rekening)")
        print("  - mtr_saving_type")
        print("  - mtr_form_template")
        print("  - trx_saving_account (berbasis user_id)")
        print("  - trx_saving_transaction")
        print("  - trx_loan (berbasis user_id)")
        print("  - trx_loan_installment")
    except Exception as e:
        print(f"\n Gagal membuat tabel: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
