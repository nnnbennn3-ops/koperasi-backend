from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func
from src.configs.database import Base


class MtrUserBankMapping(Base):
    __tablename__ = "mtr_user_bank_mapping"

    user_bank_mapping_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, nullable=False, unique=True, index=True
    )  # 1 user hanya punya 1 rekening
    bank_id = Column(Integer, nullable=False, index=True)  # ID Bank dari FinanceService
    account_number = Column(String(50), nullable=False)  # Norek isi sendiri
    created_at = Column(DateTime, nullable=False, server_default=func.sysutcdatetime())
    updated_at = Column(DateTime, nullable=True, onupdate=func.sysutcdatetime())
