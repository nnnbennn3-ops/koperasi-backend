from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.configs.database import get_db
from src.exceptions.RequestException import ResponseException
from src.payloads.responses.CommonResponse import payload_response
from src.payloads.schemas.master.SavingTypeSchema import SavingTypeResponse
from src.services.master import SavingTypeService

# JWT
# from src.utils.AuthContext import AuthContext, get_auth_context

router = APIRouter(prefix="/api/v1/master", tags=["Master: Saving Type"])


@router.get(
    "/saving-type",
    status_code=status.HTTP_200_OK,
)
def get_saving_type_by_id(
    db: Session = Depends(get_db),
    # auth: AuthContext = Depends(get_auth_context),
):
    result, err = SavingTypeService.get_saving_type_by_id(db)

    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ResponseException(500),
        )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ResponseException(404),
        )

    response_data = SavingTypeResponse.model_validate(result)
    return payload_response(200, "Success retrieve saving type", response_data)
