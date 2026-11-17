# Backend Template Python (Clean Architecture & DDD)

Plantilla de backend pura en **Python 3.11+** construida con **FastAPI** y **[uv](https://github.com/astral-sh/uv)**, diseñada sobre los principios de **Clean Architecture**, **Domain-Driven Design (DDD)** y el patrón de **Puertos y Adaptadores (Arquitectura Hexagonal)**.

Evoluciona la estructura del `backend-template` (Node.js/TypeScript) adaptándola a los estándares modernos del ecosistema Python asíncrono.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Propósito |
|---|---|---|
| **Lenguaje** | Python 3.11+ / 3.12 / 3.13 | Tipado estático con `typing`, `dataclasses` y Pydantic v2 |
| **Gestor de Paquetes** | `uv` (Astral) | Gestión ultrarrápida de entornos virtuales, dependencias y lockfile |
| **API Framework** | FastAPI + Uvicorn (ASGI) | Rutas asíncronas, validación con Pydantic y OpenAPI/Swagger automático |
| **Base de Datos** | MongoDB (Motor AsyncIO Driver) | Persistencia documental asíncrona con `MongoClientFactory` y `MongoRepository` |
| **Caché y Almacenamiento** | Redis (`redis.asyncio`) | Caché de baja latencia con `RedisClientFactory` y `RedisRepository` |
| **Logging** | Loguru (`AppLogger`) | Logging estructurado desacoplado mediante `LoggerContract` |
| **Contenedores** | Docker & Docker Compose | Entorno listo para desarrollo y producción con App, MongoDB y Redis |

---

## 🚀 Características Principales

- **Clean Architecture & DDD Puro**: Separación estricta en capas (`domain`, `application`, `infrastructure`) organizada por Bounded Contexts (`health`, `shared`).
- **Inversión de Dependencias (DIP)**: Contratos abstractos en el dominio (`HealthContract`, `LoggerContract`) desacoplados de las implementaciones concretas.
- **Contenedor de Inyección de Dependencias (DI)**: Gestión centralizada de ciclo de vida e instancias en `src/app/dependency_injection/container.py`.
- **Middlewares HTTP**:
  - `CORSMiddleware` configurado en el servidor ASGI.
  - `RequestLoggingMiddleware` con medición de latencia e inyección de cabecera `X-Process-Time`.
- **Manejo Centralizado de Errores**: Captura homogénea de excepciones de dominio (`BaseError`), errores de validación (`RequestValidationError`) y errores no controlados (`500 Internal Server Error`).
- **Health Check Asíncrono (`GET /health`)**: Verifica en tiempo real el estado del servicio y la conectividad con MongoDB y Redis.

---

## 📂 Estructura del Proyecto

```
backend-template-python/
├── src/
│   ├── app/                                 # Capa de Entrega / Presentación (FastAPI)
│   │   ├── config.py                        # Variables de entorno con pydantic-settings
│   │   ├── dependency_injection/            # Contenedor de Inyección de Dependencias
│   │   ├── middlewares/                     # Error handling y request logging
│   │   ├── routes/                          # Enrutadores HTTP
│   │   │   ├── index.py                     # Registro central de rutas
│   │   │   └── health/                      # GET /health
│   │   ├── server.py                        # Factory FastAPI y ciclo de vida ASGI (lifespan)
│   │   └── main.py                          # Entrypoint con Uvicorn
│   │
│   └── context/                             # Bounded Contexts (DDD)
│       ├── health/                          # Contexto de Salud del Sistema
│       │   ├── application/                 # HealthUseCase
│       │   ├── domain/                      # HealthContract
│       │   └── infrastructure/              # HealthRepository (chequeo MongoDB & Redis)
│       │
│       └── shared/                          # Shared Kernel
│           ├── domain/                      # BaseError, excepciones de dominio, LoggerContract
│           └── infrastructure/              # MongoClientFactory, RedisClientFactory, AppLogger
│
├── test/                                    # Pruebas unitarias y de integración
│   ├── conftest.py                          # Fixtures de FastAPI y clientes de prueba
│   └── test_health.py                       # Test de integración para GET /health
│
├── docs/                                    # Documentación técnica
│   ├── ANALISIS_ARQUITECTONICO.md           # Análisis Clean Architecture y diagramas
│   └── API_GUIDE.md                         # Guía de endpoints y ejemplos cURL
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── uv.lock
└── .env.example
```

---

## ⚡ Instalación y Puesta en Marcha

### Opción 1: Con `uv` (Recomendado)

El proyecto está configurado nativamente para **[uv](https://github.com/astral-sh/uv)** mediante `pyproject.toml` y `uv.lock`.

```bash
cd backend-template-python

# 1. Sincronizar entorno virtual y dependencias (incluyendo herramientas de desarrollo)
uv sync --extra dev

# 2. Configurar variables de entorno
cp .env.example .env    # o copy .env.example .env en Windows

# 3. Iniciar el servidor FastAPI con recarga en caliente
uv run python src/app/main.py

# 4. Ejecutar la suite de pruebas
uv run pytest -v
```

---

### Opción 2: Con Docker Compose

Inicia automáticamente FastAPI, MongoDB y Redis:

```bash
cd backend-template-python
docker-compose up --build
```

La aplicación estará disponible en:
- **API**: `http://localhost:8000`
- **Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

---

## ⚙️ Variables de Entorno Clave (`.env`)

| Variable | Descripción | Valor por Defecto |
|---|---|---|
| `APP_NAME` | Nombre del servicio | `backend-template-python` |
| `APP_ENV` | Entorno de ejecución | `development` |
| `APP_PORT` | Puerto HTTP del servidor | `8000` |
| `APP_HOST` | Host de escucha | `0.0.0.0` |
| `DEBUG` | Modo depuración con reload automático | `True` |
| `API_V1_PREFIX` | Prefijo para rutas versionadas | `/api/v1` |
| `MONGO_URI` | URI de conexión a MongoDB | `mongodb://localhost:27017` |
| `MONGO_DB_NAME` | Nombre de la base de datos en MongoDB | `backend_template_db` |
| `REDIS_HOST` | Host del servidor Redis | `localhost` |
| `REDIS_PORT` | Puerto de Redis | `6379` |

---

## 🧪 Ejecución de Pruebas

```bash
uv run pytest -v
```

---

## 📚 Documentación Adicional

- [Análisis Arquitectónico](docs/ANALISIS_ARQUITECTONICO.md): Modelo de capas, principios SOLID e inyección de dependencias.
- [Guía de la API](docs/API_GUIDE.md): Especificación del endpoint `/health` y formato de errores.
