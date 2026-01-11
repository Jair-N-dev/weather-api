# 🌤️ WeatherFast API

API REST para gestionar datos climáticos de ciudades, construida con FastAPI y MySQL.

## 🚀 Tecnologías

- Python 3.10+
- FastAPI
- SQLAlchemy
- MySQL
- Pydantic

## ✨ Características

- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Validación de datos con Pydantic
- ✅ Búsqueda por nombre de ciudad
- ✅ Filtros por condición climática
- ✅ Filtros por rango de temperatura
- ✅ Documentación interactiva automática
- ✅ Manejo de errores robusto
- ✅ Paginación en listados

## 📋 Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información de la API |
| GET | `/ciudades/` | Listar todas las ciudades (paginado) |
| GET | `/ciudades/{nombre}` | Buscar ciudad por nombre |
| POST | `/ciudades/` | Crear nueva ciudad |
| PUT | `/ciudades/{ciudad_id}` | Actualizar ciudad existente |
| DELETE | `/ciudades/{ciudad_id}` | Eliminar ciudad |
| GET | `/ciudades/clima/{condicion}` | Filtrar por condición climática |
| GET | `/ciudades/temperatura/rango` | Filtrar por rango de temperatura |

## 🔧 Instalación

### 1. Clonar repositorio
```bash
git clone https://github.com/Jair-N-dev/weather-api.git
cd weather-api
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos

Crear base de datos en MySQL:
```sql
CREATE DATABASE weather_db;
```

Crear archivo `.env` en la raíz del proyecto:
```env
DATABASE_URL=mysql+pymysql://usuario:password@localhost/weather_db
```

### 5. Poblar datos iniciales (opcional)
```bash
python seed.py
```

### 6. Ejecutar servidor
```bash
uvicorn main:app --reload
```

La API estará disponible en: http://localhost:8000

## 📚 Documentación

Una vez el servidor esté corriendo:

- **Swagger UI (interactiva):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 💡 Ejemplos de uso

### Crear ciudad
```bash
curl -X POST http://localhost:8000/ciudades/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Medellín",
    "temp": 24,
    "condicion": "Parcialmente nublado",
    "humedad": 70
  }'
```

### Buscar ciudad
```bash
curl http://localhost:8000/ciudades/medellin
```

### Filtrar por temperatura
```bash
curl "http://localhost:8000/ciudades/temperatura/rango?temp_min=20&temp_max=30"
```

### Actualizar ciudad
```bash
curl -X PUT http://localhost:8000/ciudades/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Medellín",
    "temp": 26,
    "condicion": "Soleado",
    "humedad": 65
  }'
```

### Eliminar ciudad
```bash
curl -X DELETE http://localhost:8000/ciudades/1
```

## 📁 Estructura del proyecto
```
weather-api/
├── main.py           # Endpoints de la API
├── database.py       # Configuración de base de datos
├── models.py         # Modelos SQLAlchemy
├── schemas.py        # Esquemas Pydantic
├── seed.py           # Datos iniciales
├── .env              # Variables de entorno (no incluido en repo)
├── .gitignore
├── requirements.txt
└── README.md
```

## 🛠️ Tecnologías utilizadas

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para Python
- **Pydantic**: Validación de datos
- **MySQL**: Base de datos relacional
- **Uvicorn**: Servidor ASGI

## 📝 Próximas mejoras

- [x] Agregar Base de datos Mysql
- [ ] Agregar autenticación JWT
- [ ] Implementar tests con Pytest
- [ ] Deploy en Railway/Render
- [ ] Agregar caché con Redis

## 👤 Autor

[Jair] - [GitHub](https://github.com/Jair-N-dev) 