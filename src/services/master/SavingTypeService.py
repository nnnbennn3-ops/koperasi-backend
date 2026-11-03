from sqlalchemy.orm import Session
from src.repositories.master import SavingTypeRepo


def get_saving_type_by_id(db: Session):
    data, err = SavingTypeRepo.get_saving_type_by_id(db)
    return data, err
