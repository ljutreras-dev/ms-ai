# Guía de la API - Backend Template Python

Documentación de referencia para los endpoints base de la plantilla FastAPI.

- **Base URL**: `http://localhost:8000`
- **Prefijo de API v1**: `/api/v1`
- **Documentación Interactiva Swagger**: `http://localhost:8000/docs`
- **Documentación ReDoc**: `http://localhost:8000/redoc`

---

## 1. Verificación de Salud (Health Check)

### `GET /health`
Verifica la disponibilidad general del servicio y la conectividad asíncrona con MongoDB y Redis.

**Ejemplo cURL:**
```bash
curl -X GET http://localhost:8000/health
```

**Respuesta Exitosa (`200 OK`):**
```json
{
  "status": "UP",
  "service": "backend-template-python",
  "version": "1.0.0",
  "uptime_seconds": 12.45,
  "dependencies": {
    "mongodb": "UP",
    "redis": "UP"
  }
}
```

> Si MongoDB o Redis no están disponibles, el endpoint responde con `"status": "DEGRADED"` e indica `"DOWN"` en la dependencia correspondiente sin interrumpir el servicio.

---

## 2. Formato Estándar de Errores

Los middlewares de manejo de errores (`src/app/middlewares/error_handler.py`) estandarizan todas las respuestas de error:

- **Errores de Dominio (`BaseError`)**:
  ```json
  {
    "error": "Resource not found"
  }
  ```
- **Errores de Validación (`422 Unprocessable Entity`)**:
  ```json
  {
    "message": "Validation Error",
    "errors": [
      {
        "field": "body -> field_name",
        "message": "Field required",
        "type": "missing"
      }
    ]
  }
  ```
- **Errores No Controlados (`500 Internal Server Error`)**:
  ```json
  {
    "error": "Internal Server Error",
    "message": "An unexpected error occurred."
  }
  ```
