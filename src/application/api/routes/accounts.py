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


# 📦 SCHEMAS

class CreateAccountRequest(BaseModel):
    owner: str
    initial_balance: Decimal


class AccountResponse(BaseModel):
    id: int
    owner: str
    balance: Decimal


# 🚀 ENDPOINTS

@router.post("/", response_model=AccountResponse)
def create_account(
    request: CreateAccountRequest,
    db: Session = Depends(get_db)
):
    service = AccountRepository(
        repository=AccountRepositoryImpl(),
        db=db  # (lo vamos a eliminar más adelante)
    )

    try:
        account = service.create_account(
            request.owner,
            request.initial_balance
        )
        db.commit()

        return AccountResponse(
            id=account.id,
            owner=account.owner,
            balance=account.balance
        )

    except Exception as e:
        db.rollback()
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    service = AccountRepository(
        repository=AccountRepositoryImpl(),
        db=db
    )

    account = service.get_account(account_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    return AccountResponse(
        id=account.id,
        owner=account.owner,
        balance=account.balance
    )