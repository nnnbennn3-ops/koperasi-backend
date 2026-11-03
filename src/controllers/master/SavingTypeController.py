from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.configs.database import get_db
from src.payloads.schemas.master.SavingTypeSchema import CommonResponse
from src.services.master import SavingTypeService

# JWT
# from src.utils.AuthContext import AuthContext, get_auth_context

router = APIRouter(prefix="/api/v1/master", tags=["Master: Saving Type"])


@router.get(
    "/saving-type",
    response_model=CommonResponse,
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
            detail=f"Database error: {str(err)}",
        )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data saving type tidak ditemukan",
        )

    return CommonResponse(
        status_code=200,
        message="Success",
        data=result,
    )
