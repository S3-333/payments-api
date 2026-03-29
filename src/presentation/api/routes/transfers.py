# =============================================================================
# POST /transfers/ — mismo patrón que accounts: sesión + caso de uso inyectados.
# La ruta no sabe nada de SQL ni de FOR UPDATE; eso está en repositorio + caso de uso.
# =============================================================================

from decimal import Decimal

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.application.use_cases.transfer_money import TransferMoneyUseCase
from src.presentation.api.deps import get_db, get_transfer_money_use_case

router = APIRouter()


class TransferRequest(BaseModel):
    """JSON de entrada; Field(gt=0) evita montos cero/negativos antes de llegar al dominio."""

    from_account_id: int = Field(..., ge=1)
    to_account_id: int = Field(..., ge=1)
    amount: Decimal = Field(..., gt=0, description="Monto estrictamente positivo")


class TransferResponse(BaseModel):
    status: str = "success"


@router.post("/", response_model=TransferResponse)
def transfer_money(
    request: TransferRequest,
    db: Session = Depends(get_db),
    use_case: TransferMoneyUseCase = Depends(get_transfer_money_use_case),
) -> TransferResponse:
    """
    Ejecuta transferencia atómica: bloqueo ordenado, validación de saldo, registro en ledger.

    DomainError -> 400; errores de servidor sin capturar -> 500 (FastAPI por defecto).
    """
    # Todos los argumentos ya vienen validados por Pydantic (tipos y gt=0)
    use_case.execute(
        db,
        request.from_account_id,
        request.to_account_id,
        request.amount,
    )
    return TransferResponse()
