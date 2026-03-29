from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal
from pydantic import BaseModel

from src.application.api.deps import get_db
from src.domain.services.account_service import AccountRepository
from src.infrastructure.database.repositories.account_repository_impl import (
    AccountRepositoryImpl,
)

router = APIRouter()


# 📦 SCHEMA

class TransferRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: Decimal


# 🚀 ENDPOINT

@router.post("/")
def transfer_money(
    request: TransferRequest,
    db: Session = Depends(get_db)
):
    service = AccountRepository(
        repository=AccountRepositoryImpl(),
        db=db  # (lo vamos a eliminar en el próximo refactor)
    )

    try:
        service.transfer_money(
            request.from_account_id,
            request.to_account_id,
            request.amount
        )

        db.commit()

        return {"status": "success"}

    except ValueError as e:
        print("ERROR:", e)
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        db.rollback()
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))