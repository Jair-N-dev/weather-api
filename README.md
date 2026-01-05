# Weather API

REST API para gestionar datos climáticos de ciudades, construida con FastAPI.

## Tecnologías

- Python 3.10+
- FastAPI
- Pydantic
- Uvicorn

## Características

- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Validación de datos con Pydantic
- ✅ Documentación interactiva automática
- ✅ Manejo de errores HTTP
- ✅ Códigos de estado HTTP correctos

## Instalación
```bash Jair-N-dev
# Clonar repositorio
git clone https://github.com/Jair-N-dev/weather-api.git
cd weather-api

# Instalar dependencias
pip install fastapi uvicorn

# Ejecutar servidor
uvicorn main:app --reload
```

## Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información de la API |
| GET | `/ciudades/` | Listar todas las ciudades |
| GET | `/clima/?ciudad={nombre}` | Obtener clima de una ciudad |
| POST | `/agregar-clima/` | Agregar nueva ciudad |
| PUT | `/actualizar-clima/{ciudad}` | Actualizar datos de ciudad |
| DELETE | `/eliminar-clima/{ciudad}` | Eliminar ciudad |

## Documentación

Una vez ejecutando el servidor, accede a:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Ejemplo de uso
```bash
# Obtener clima de Bogotá
curl http://localhost:8000/clima/?ciudad=bogota

# Agregar nueva ciudad
curl -X POST http://localhost:8000/agregar-clima/ \
  -H "Content-Type: application/json" \
  -d '{
    "ciudad": "Medellín",
    "temp": 24,
    "condicion": "Parcialmente nublado",
    "humedad": 70
  }'
```

## Próximas mejoras

- [ ] Conectar con base de datos MySQL
- [ ] Agregar autenticación JWT
- [ ] Implementar tests con Pytest
- [ ] Deploy en Railway/Render

## Autor

Jair 