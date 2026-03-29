# =============================================================================
# Punto de entrada que suele usar uvicorn:  uvicorn src.application.main:app --reload
#
# ¿Por qué este archivo es tan corto? Para no duplicar la app FastAPI: la definición
# real (routers, exception handlers) está en src/presentation/main.py.
# Así solo cambias un sitio si añades rutas o middleware.
# =============================================================================

from src.presentation.main import app

__all__ = ["app"]
