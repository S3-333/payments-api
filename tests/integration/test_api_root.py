# Smoke test HTTP sin base de datos: verifica que la app FastAPI arranca y responde.

from fastapi.testclient import TestClient

from src.presentation.main import app


def test_root_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "API running"
