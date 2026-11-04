from sqlalchemy.orm import Session
from src.payloads.schemas.transaction.DashboardSchema import (
    DashboardDataResponse,
    MonthGroupTransactionResponse,
    SaldoSummaryResponse,
    TransactionItemResponse,
    UserSummaryResponse,
)
from src.repositories.transaction import DashboardRepo
from src.utils.CrossServiceHelper import safe_fetch_dict
from src.utils.MonthNames import IndonesianMonth
from src.utils.ServicesRequest import ServiceClient

cross_service = ServiceClient()


def get_dashboard_summary(
    db: Session,
    page: int,
    limit: int,
    authorization: str,
    user_id: int,
    month: int | None = None,
    year: int | None = None,
):
    # Ambil nama dari general service
    user_detail = (
        safe_fetch_dict(
            cross_service.general,
            f"user-detail?user_id={user_id}&is_cross=true",
            ["employee_name", "id_number"],
            headers=authorization,
        )
        or {}
    )
    user_name = user_detail.get("employee_name") or "Anggota Koperasi"
    member_id = str(user_detail.get("id_number") or user_id)

    # Ambil rekening simpanan dari db koperasi
    savings_raw, err = DashboardRepo.get_user_saving_accounts(db, user_id)
    if err is not None:
        return None, None, err

    if not savings_raw:
        return None, None, "NOT_FOUND"

    saldo_map = {"pokok": 0.0, "wajib": 0.0, "sukarela": 0.0}
    total_saldo = 0.0

    for account, type_code in savings_raw:
        balance = float(account.current_balance)
        code_lower = str(type_code).lower()
        if "pokok" in code_lower:
            saldo_map["pokok"] = balance
        elif "wajib" in code_lower:
            saldo_map["wajib"] = balance
        elif "sukarela" in code_lower:
            saldo_map["sukarela"] = balance
        total_saldo += balance

    # Ambil transaksi paginated & kelompokkan per bulan
    transactions_raw, pagination, err = DashboardRepo.get_user_transactions(
        db, user_id, page=page, limit=limit, month=month, year=year
    )
    if err is not None:
        return None, None, err

    groups_dict = {}

    for trx in transactions_raw:
        item = TransactionItemResponse(
            type="deposit" if trx.is_credit else "withdraw",
            title=trx.transaction_description,
            date=trx.transaction_date,
            amount=float(trx.amount),
        )

        month_name = IndonesianMonth.to_name(trx.transaction_date.month)
        month_label = f"{month_name} {trx.transaction_date.year}"

        if month_label not in groups_dict:
            groups_dict[month_label] = {
                "month": month_label,
                "deposit": 0.0,
                "withdraw": 0.0,
                "transactions": [],
            }

        if trx.is_credit:
            groups_dict[month_label]["deposit"] += float(trx.amount)
        else:
            groups_dict[month_label]["withdraw"] += float(trx.amount)

        groups_dict[month_label]["transactions"].append(item)

    monthly_transactions = [
        MonthGroupTransactionResponse(**group) for group in groups_dict.values()
    ]

    dashboard_data = DashboardDataResponse(
        user=UserSummaryResponse(name=user_name, member_id=member_id),
        saldo=SaldoSummaryResponse(
            pokok=saldo_map["pokok"],
            wajib=saldo_map["wajib"],
            sukarela=saldo_map["sukarela"],
            total=total_saldo,
        ),
        monthly_transactions=monthly_transactions,
    )

    return dashboard_data, pagination, None
