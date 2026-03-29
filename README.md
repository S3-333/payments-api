# API REST — Motor de pagos (cuentas y transferencias)

Backend en **FastAPI** con **SQLAlchemy**, **MySQL**, reglas de negocio en capas (dominio / aplicación / infraestructura / presentación), bloqueo de filas para transferencias y migraciones con **Alembic**.

---

## Tabla de contenidos

- [Características](#características)
- [Stack](#stack)
- [Requisitos](#requisitos)
- [Puesta en marcha](#puesta-en-marcha)
- [Variables de entorno](#variables-de-entorno)
- [Base de datos y Alembic](#base-de-datos-y-alembic)
- [Ejecutar la API](#ejecutar-la-api)
- [Probar la API](#probar-la-api)
- [Tests](#tests)
- [Estructura del proyecto](#estructura-del-proyecto)
- [CI/CD](#cicd)
- [Licencia](#licencia)

---

## Características

- Crear cuentas y consultar saldos
- Transferencias entre cuentas con transacciones SQL y bloqueo ordenado de filas (`SELECT ... FOR UPDATE`)
- Registro de movimientos en tabla de auditoría (`transfer_records`)
- Value object `Money` basado en `Decimal`
- Manejo centralizado de errores de dominio (HTTP 400/404)

---

## Stack

| Componente | Uso |
|------------|-----|
| Python 3.11+ | Lenguaje |
| FastAPI | API HTTP |
| Pydantic v2 | Validación de entrada/salida |
| SQLAlchemy 2.x | ORM |
| PyMySQL | Driver MySQL |
| Alembic | Migraciones de esquema |
| Docker Compose | MySQL 8 en desarrollo |
| Pytest + httpx | Tests |

---

## Requisitos

- **Python** 3.11 o superior
- **Docker** y Docker Compose (para MySQL local), o una instancia MySQL accesible
- Git

---

## Puesta en marcha

```bash
# Clonar (tras crear el repo en GitHub)
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO

# Entorno virtual
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

pip install -r requirements.txt
```

### MySQL con Docker

```bash
docker compose up -d
```

Espera unos segundos a que el contenedor esté listo (puerto **3306**).

### Configuración

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/macOS
```

Edita `.env` y asegúrate de que `DATABASE_URL` coincida con usuario, contraseña, host y base definidos en `docker-compose.yml` (por defecto: usuario `user`, contraseña `password`, base `payments`).

**No subas `.env` al repositorio** (ya está en `.gitignore`). Solo `.env.example` es la plantilla sin secretos reales.

---

## Variables de entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `DATABASE_URL` | Cadena SQLAlchemy para MySQL | `mysql+pymysql://user:password@localhost:3306/payments` |
| `SQL_ECHO` | Si es `true`, imprime SQL en consola (solo desarrollo) | `false` |

---

## Base de datos y Alembic

Aplicar el esquema (tablas `accounts`, `transfer_records`):

```bash
alembic upgrade head
```

La migración inicial está pensada para no fallar si las tablas ya existían (por ejemplo tras pruebas con `create_all`); igual conviene usar siempre Alembic como fuente de verdad del esquema.

---

## Ejecutar la API

```bash
uvicorn src.application.main:app --reload
```

- API: `http://127.0.0.1:8000`
- Documentación interactiva (Swagger): `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

---

## Probar la API

1. **POST** `/accounts/` — crea cuentas (por ejemplo dos, con `owner` y `initial_balance` ≥ 0).
2. **POST** `/transfers/` — usa los `id` devueltos como `from_account_id` y `to_account_id`, y un `amount` > 0.
3. **GET** `/accounts/{account_id}` — comprueba saldos.

`initial_balance` puede enviarse como número JSON sin comillas (recomendado).

---

## Tests

```bash
pytest tests -v
```

Los tests de integración usan **SQLite** en memoria o archivo temporal; **no dependen** de MySQL para ejecutarse en local o en CI.

---

## Estructura del proyecto

```
├── alembic/                 # Migraciones Alembic
├── src/
│   ├── application/         # Casos de uso (orquestación)
│   ├── domain/              # Entidades, value objects, interfaces de repositorio
│   ├── infrastructure/      # ORM, implementaciones de repositorios, sesión BD
│   └── presentation/        # FastAPI: rutas, deps, manejo de errores HTTP
├── tests/                   # Unitarios e integración
├── docker-compose.yml       # Servicio MySQL 8
├── requirements.txt
├── pytest.ini
└── .env.example
```

---

## CI/CD

- **GitHub Actions** (`.github/workflows/ci.yml`): en cada push o PR a `main`/`master` ejecuta `pytest` en Python 3.11 y 3.12.
- **Dependabot** (`.github/dependabot.yml`): propone actualizaciones mensuales de dependencias Pip y de las acciones de GitHub.

Tras el primer push, actualiza el badge del README con la URL real de tu repositorio.

---

## Licencia

Este proyecto se distribuye bajo la licencia **MIT** (ver archivo [LICENSE](LICENSE)).

---

## Contribuciones

1. Fork del repositorio
2. Rama desde `main` (`feature/...`)
3. Cambios con tests en verde (`pytest`)
4. Pull request describiendo el cambio

Mantén fuera del control de versiones credenciales y archivos `.env`.
