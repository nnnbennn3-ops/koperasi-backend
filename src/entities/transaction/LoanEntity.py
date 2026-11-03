from sqlalchemy import (
    Column,
    Date,
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


class TrxLoan(Base):
    __tablename__ = "trx_loan"

    loan_id = Column(Integer, primary_key=True, autoincrement=True)
    loan_number = Column(String(50), nullable=False, unique=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # Cross-service ID
    total_loan = Column(Numeric(18, 2), nullable=False)
    interest_rate_percent = Column(Numeric(5, 2), nullable=False, default=1.00)
    tenor_months = Column(Integer, nullable=False)
    monthly_installment = Column(Numeric(18, 2), nullable=False)
    principal_paid = Column(Numeric(18, 2), nullable=False, default=0.00)
    remaining_loan = Column(Numeric(18, 2), nullable=False)
    status = Column(String(20), nullable=False, default="active")
    start_date = Column(Date, nullable=False)
    next_payment_date = Column(Date, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.sysutcdatetime())

    # relationships lokal
    installments = relationship(
        "TrxLoanInstallment",
        back_populates="loan",
        foreign_keys="TrxLoanInstallment.loan_id",
    )


class TrxLoanInstallment(Base):
    __tablename__ = "trx_loan_installment"
    __table_args__ = (
        UniqueConstraint("loan_id", "installment_no", name="uq_loan_installment_no"),
    )

    installment_id = Column(Integer, primary_key=True, autoincrement=True)
    loan_id = Column(Integer, ForeignKey("trx_loan.loan_id"), nullable=False)
    installment_no = Column(Integer, nullable=False)
    due_date = Column(Date, nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    paid_date = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False, default="unpaid")
    created_at = Column(DateTime, nullable=False, server_default=func.sysutcdatetime())

    loan = relationship(
        "TrxLoan", back_populates="installments", foreign_keys=[loan_id]
    )
