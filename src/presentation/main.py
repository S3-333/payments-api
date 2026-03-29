# =============================================================================
# Capa de presentación (HTTP):
# - Crea el objeto FastAPI
# - Registra las rutas (routers) de accounts y transfers
# - Traduce errores de dominio a códigos HTTP (400/404) en un solo sitio
#
# Flujo típico de una petición:  cliente HTTP
#   -> router en routes/*.py
#   -> Depends(get_db) abre sesión SQL
#   -> Depends(get_*_use_case) inyecta el caso de uso
#   -> caso de uso llama al repositorio (infraestructura)
#   -> si hay DomainError, llega aquí al exception_handler
# =============================================================================

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.domain.exceptions import AccountNotFoundError, DomainError
from src.presentation.api.routes import accounts, transfers

# Instancia principal de la API (documentación automática en /docs)
app = FastAPI(
    title="Payments API",
    description="Motor de pagos concurrentes (cuentas, saldos, transferencias con bloqueo de filas).",
    version="1.0.0",
)

# prefix: todas las rutas de accounts quedan bajo /accounts/...
app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(transfers.router, prefix="/transfers", tags=["transfers"])


@app.get("/")
def root() -> dict[str, str]:
    # Endpoint mínimo para comprobar que el proceso está vivo (smoke test)
    return {"message": "API running"}


@app.exception_handler(DomainError)
async def domain_error_handler(_: Request, exc: DomainError) -> JSONResponse:
    """
    Errores de dominio: 404 si la cuenta no existe; 400 para el resto de reglas de negocio.

    AccountNotFoundError hereda de DomainError: si registráramos solo DomainError sin distinguir,
    un 404 se convertiría en 400. Por eso se usa isinstance aquí.
    """
    if isinstance(exc, AccountNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})
    return JSONResponse(status_code=400, content={"detail": str(exc)})
