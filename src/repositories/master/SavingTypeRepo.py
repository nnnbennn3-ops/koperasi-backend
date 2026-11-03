from sqlalchemy import select
from sqlalchemy.orm import Session
from src.entities.master.SavingTypeEntity import MtrSavingType


def get_saving_type_by_id(db: Session):
    try:
        query = select(MtrSavingType).where(MtrSavingType.saving_type_id == 1)

        result = db.scalars(query).first()
        return result, None
    except Exception as err:
        return None, err
