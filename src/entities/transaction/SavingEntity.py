from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.configs.database import Base

# Tambahkan ini di bagian atas SavingEntity.py
from src.entities.master.SavingTypeEntity import MtrSavingType


class TrxSavingAccount(Base):
    __tablename__ = "trx_saving_account"
    __table_args__ = (
        UniqueConstraint("user_id", "saving_type_id", name="uq_user_saving_type"),
    )

    saving_account_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)  # Cross-service ID
    saving_type_id = Column(
        Integer, ForeignKey("mtr_saving_type.saving_type_id"), nullable=False
    )
    current_balance = Column(Numeric(18, 2), nullable=False, default=0.00)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.sysutcdatetime())

    saving_type = relationship("MtrSavingType", foreign_keys=[saving_type_id])
    transactions = relationship(
        "TrxSavingTransaction",
        back_populates="saving_account",
        foreign_keys="TrxSavingTransaction.saving_account_id",
    )


class TrxSavingTransaction(Base):
    __tablename__ = "trx_saving_transaction"

    saving_trx_id = Column(Integer, primary_key=True, autoincrement=True)
    saving_account_id = Column(
        Integer, ForeignKey("trx_saving_account.saving_account_id"), nullable=False
    )
    transaction_description = Column(String(255), nullable=False)
    is_credit = Column(Boolean, nullable=False)  # True (+ Masuk), False (- Keluar)
    amount = Column(Numeric(18, 2), nullable=False)
    transaction_date = Column(
        DateTime, nullable=False, server_default=func.sysutcdatetime()
    )
    notes = Column(String(255), nullable=True)

    saving_account = relationship(
        "TrxSavingAccount",
        back_populates="transactions",
        foreign_keys=[saving_account_id],
    )
