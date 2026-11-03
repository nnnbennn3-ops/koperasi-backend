from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.configs.database import Base


class MtrFormTemplate(Base):
    __tablename__ = "mtr_form_template"

    form_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True)
    file_path = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.sysutcdatetime())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.sysutcdatetime(),
        onupdate=func.sysutcdatetime(),
    )
