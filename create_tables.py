import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.configs.database import Base, engine

from src.entities.master.FormEntity import MtrFormTemplate
from src.entities.master.SavingTypeEntity import MtrSavingType
from src.entities.master.UserBankMappingEntity import MtrUserBankMapping
from src.entities.transaction.LoanEntity import TrxLoan, TrxLoanInstallment
from src.entities.transaction.SavingEntity import TrxSavingAccount, TrxSavingTransaction


def main():
    print("Menghubungkan ke SQL Server 2022 (kopkar)")
    try:
        Base.metadata.create_all(bind=engine)

        print("\n SUKSES! Seluruh tabel siap digunakan:")
        print("  - mtr_user_bank_mapping")
        print("  - mtr_saving_type")
        print("  - mtr_form_template")
        print("  - trx_saving_account")
        print("  - trx_saving_transaction")
        print("  - trx_loan")
        print("  - trx_loan_installment")

    except Exception as e:
        print(f"\n Gagal membuat tabel: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
