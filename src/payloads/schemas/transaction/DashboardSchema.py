from datetime import datetime
from pydantic import BaseModel


class UserSummaryResponse(BaseModel):
    name: str
    member_id: str


class SaldoSummaryResponse(BaseModel):
    pokok: float = 0.0
    wajib: float = 0.0
    sukarela: float = 0.0
    total: float = 0.0


class TransactionItemResponse(BaseModel):
    type: str
    title: str
    date: datetime
    amount: float


class MonthGroupTransactionResponse(BaseModel):
    month: str
    deposit: float = 0.0
    withdraw: float = 0.0
    transactions: list[TransactionItemResponse] = []


class DashboardDataResponse(BaseModel):
    user: UserSummaryResponse
    saldo: SaldoSummaryResponse
    monthly_transactions: list[MonthGroupTransactionResponse] = []
