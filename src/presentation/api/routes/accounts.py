# =============================================================================
# Rutas HTTP de /accounts: capa delgada.
# - Pydantic valida JSON de entrada/salida
# - Los casos de uso contienen reglas de negocio y transacciones
# - No hacemos db.commit() aquí: eso va dentro del caso de uso correspondiente
# =============================================================================

from decimal import Decimal

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.application.use_cases.create_account import CreateAccountUseCase
from src.application.use_cases.get_account import GetAccountUseCase
from src.presentation.api.deps import (
    get_create_account_use_case,
    get_db,
    get_get_account_use_case,
)

router = APIRouter()


class CreateAccountRequest(BaseModel):
    """Cuerpo JSON esperado en POST /accounts/ (validación antes de tocar la base)."""

    owner: str = Field(..., min_length=1, max_length=100, description="Titular de la cuenta")
    initial_balance: Decimal = Field(
        default=Decimal("0"),
        ge=0,
        description="Saldo inicial (>= 0); Decimal evita errores de float",
    )


class AccountResponse(BaseModel):
    """Cuerpo JSON de respuesta: lo que el cliente recibe (no es la entidad de dominio cruda)."""

    id: int
    owner: str
    balance: Decimal

    model_config = {"from_attributes": True}


@router.post("/", response_model=AccountResponse)
def create_account(
    request: CreateAccountRequest,
    db: Session = Depends(get_db),
    use_case: CreateAccountUseCase = Depends(get_create_account_use_case),
) -> AccountResponse:
    """
    POST /accounts/
    1) FastAPI valida request con CreateAccountRequest
    2) get_db entrega la sesión SQL abierta para esta petición
    3) get_create_account_use_case construye el caso de uso con el repositorio real
    4) execute(...) crea la fila y hace commit dentro del caso de uso
    """
    account = use_case.execute(db, request.owner, request.initial_balance)
    # account es entidad de dominio; convertimos a DTO para la respuesta HTTP
    return AccountResponse(
        id=account.id,
        owner=account.owner,
        balance=account.balance.amount,
    )


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: int,
    db: Session = Depends(get_db),
    use_case: GetAccountUseCase = Depends(get_get_account_use_case),
) -> AccountResponse:
    # GET solo lee datos: el caso de uso no hace commit (no hay cambios que guardar)
    account = use_case.execute(db, account_id)
    return AccountResponse(
        id=account.id,
        owner=account.owner,
        balance=account.balance.amount,
    )
