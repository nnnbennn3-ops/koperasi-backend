from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from src.configs.database import Base


class MtrSavingType(Base):
    __tablename__ = "mtr_saving_type"

    saving_type_id = Column(Integer, primary_key=True, autoincrement=True)
    saving_type_code = Column(String(20), nullable=False, unique=True, index=True)
    saving_type_name = Column(String(50), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    saving_accounts = relationship(
        "TrxSavingAccount",
        back_populates="saving_type",
        foreign_keys="TrxSavingAccount.saving_type_id",
    )
