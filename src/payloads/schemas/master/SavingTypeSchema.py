from pydantic import BaseModel, ConfigDict


class SavingTypeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    saving_type_id: int
    saving_type_code: str
    saving_type_name: str
    is_active: bool


class CommonResponse(BaseModel):
    status_code: int = 200
    message: str = "Success"
    data: SavingTypeResponse | None = None
