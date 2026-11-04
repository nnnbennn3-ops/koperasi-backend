from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.configs.database import get_db
from src.exceptions.RequestException import ResponseException
from src.payloads.responses.PaginationResponse import pagination_response
from src.services.transaction import DashboardService
from src.utils.AuthContext import AuthContext, get_auth_context

router = APIRouter(tags=["Transaction : Dashboard"], prefix="/v1")


@router.get("/dashboard/summary", status_code=status.HTTP_200_OK)
def get_dashboard_summary(
    page: int = 1,
    limit: int = 10,
    month: int | None = None,
    year: int | None = None,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(get_auth_context),
):
    """Mengambil ringkasan saldo simpanan dan riwayat transaksi anggota."""
    get_results, pages, err = DashboardService.get_dashboard_summary(
        db=db,
        page=page,
        limit=limit,
        authorization=auth.authorization,
        user_id=auth.user_id,
        month=month,
        year=year,
    )

    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ResponseException(404),
        )

    return pagination_response(
        status_code=200,
        message="Success",
        page=page,
        page_limit=limit,
        npages=pages["total_pages"],
        nrows=pages["total_rows"],
        data=get_results,
    )
