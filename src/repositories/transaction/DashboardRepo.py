import math
from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session
from src.entities.master.SavingTypeEntity import MtrSavingType
from src.entities.transaction.SavingEntity import (
    TrxSavingAccount,
    TrxSavingTransaction,
)


def get_user_saving_accounts(db: Session, user_id: int):
    """Mengambil semua akun simpanan aktif milik user."""
    try:
        query = (
            select(TrxSavingAccount, MtrSavingType.saving_type_code)
            .join(
                MtrSavingType,
                TrxSavingAccount.saving_type_id == MtrSavingType.saving_type_id,
            )
            .where(
                TrxSavingAccount.user_id == user_id,
                TrxSavingAccount.is_active == True,
            )
        )
        result = db.execute(query).all()
        return result, None
    except Exception as err:
        return None, err


def get_user_transactions(
    db: Session,
    user_id: int,
    page: int = 1,
    limit: int = 10,
    month: int | None = None,
    year: int | None = None,
):
    """Mengambil riwayat transaksi simpanan user dengan pagination dan filter bulan/tahun."""
    try:
        query = (
            select(TrxSavingTransaction)
            .join(
                TrxSavingAccount,
                TrxSavingTransaction.saving_account_id
                == TrxSavingAccount.saving_account_id,
            )
            .where(TrxSavingAccount.user_id == user_id)
        )

        if month is not None:
            query = query.where(
                extract("month", TrxSavingTransaction.transaction_date) == month
            )
        if year is not None:
            query = query.where(
                extract("year", TrxSavingTransaction.transaction_date) == year
            )

        query_count = select(func.count()).select_from(query.subquery())
        total_rows = db.scalar(query_count) or 0

        offset_val = (page - 1) * limit if page > 0 else 0
        total_pages = math.ceil(total_rows / limit) if limit > 0 else 1

        query_paginated = (
            query.order_by(TrxSavingTransaction.transaction_date.desc())
            .offset(offset_val)
            .limit(limit)
        )

        results = db.scalars(query_paginated).all()

        page_results = {
            "total_rows": total_rows,
            "total_pages": total_pages,
        }

        return results, page_results, None
    except Exception as err:
        return None, None, err
