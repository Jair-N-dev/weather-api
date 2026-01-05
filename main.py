from fastapi import FastAPI, HTTPException, status
from typing import Optional
from pydantic import BaseModel, Field

app = FastAPI(title="WeatherFast API")

# Base de datos simulada (Diccionario)
clima_db = {
    "madrid": {"temp": 25, "condicion": "Soleado", "humedad": 40},
    "bogota": {"temp": 18, "condicion": "Nublado", "humedad": 70},
    "mexico": {"temp": 22, "condicion": "Despejado", "humedad": 30},
    "buenos_aires": {"temp": 20, "condicion": "Lluvia", "humedad": 85}
}

# Validación de datos con Pydantic
class CiudadClima(BaseModel):
    ciudad: str = Field(..., min_length=2, max_length=50, description="Nombre de la ciudad")
    temp: int = Field(..., ge=-50, le=60, description="Temperatura en grados Celsius")
    condicion: str = Field(..., min_length=3, description="Condición climática")
    humedad: int = Field(..., ge=0, le=100, description="Humedad en porcentaje")
    # Ejemplo de datos
    class Config:
        json_schema_extra = {   
            "ejemplo": {
                "ciudad": "Barcelona",
                "temp": 23,
                "condicion": "Parcialmente nublado",
                "humedad": 65
            }
        }

# 0. Endpoint raíz (Información de la API)
@app.get("/")
async def root():
    """
    Endpoint raíz - Información de la API.
    """
    return {
        "api": "WeatherFast API",
        "version": "1.0",
        "endpoints": {
            "clima": "/clima/?ciudad={nombre}",
            "ciudades": "/ciudades/",
            "actualizar": "/actualizar-clima/{ciudad}",
            "eliminar": "/eliminar-clima/{ciudad}",
            "reporte": "/reporte/{ciudad}",
            "agregar": "/agregar-clima/",
        }
    }

# 1. Endpoint con Path Parameter (Mostar todas las ciudades)
@app.get("/ciudades/", tags=["Consultas"])
async def listar_ciudades():
    """
    Devuelve la lista completa de ciudades disponibles.
    """
    if not clima_db:
        return {"mensaje": "No hay ciudades registradas", "ciudades": []}
    
    return {"total": len(clima_db), "ciudades": list(clima_db.keys())}

# 2. Endpoint con Query Parameter (Para buscar)
# URL: /clima/?ciudad=madrid
@app.get("/clima/", tags=["Consultas"])
async def obtener_clima(ciudad: str):
    """
    Busca el clima de una ciudad. 
    'ciudad' es un query parameter obligatorio.
    """
    ciudad_normalizada = ciudad.lower().strip().replace(" ", "_")
    
    if ciudad_normalizada not in clima_db:
        # Si la ciudad no existe, devolvemos un error 404
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    
    return {"ciudad": ciudad, "datos": clima_db[ciudad_normalizada]}

# 3. Endpoint con Path Parameter (Para detalles técnicos)
# URL: /reporte/madrid
@app.get("/reporte/{ciudad}", tags=["Consultas"])
async def generar_reporte(ciudad: str, detalle: bool = False):
    """
    Genera un reporte detallado. 
    'ciudad' es Path Parameter.
    'detalle' es un Query Parameter opcional (booleano).
    """
    ciudad_normalizada = ciudad.lower()
    if ciudad_normalizada in clima_db:
        datos = clima_db[ciudad_normalizada]
        if detalle:
            return {
                "reporte": f"Reporte completo para {ciudad}",
                "datos": datos,
                "viento": "15km/h",
                "presion": "1013 hPa"
            }
        return {"reporte": f"Resumen para {ciudad}", "temperatura": datos["temp"]}
    
    raise HTTPException(status_code=404, detail="No hay reporte disponible")

# 4. Endpoint con Query Parameter (Para agregar)
# URL: /agregar-clima/
@app.post("/agregar-clima/", status_code=status.HTTP_201_CREATED, tags=["Modificaciones"])
async def agregar_clima(datos_ciudad: CiudadClima):
    """
    Agrega una nueva ciudad usando el Request Body (JSON).
    """
    # Convertimos el nombre a minúsculas para mantener consistencia en la DB
    nombre_ciudad = datos_ciudad.ciudad.lower().strip()

    if nombre_ciudad in clima_db:
        raise HTTPException(status_code=400, detail="La ciudad ya existe")

    # 3. Accedemos a los datos usando Pydantic
    clima_db[nombre_ciudad] = {
        "temp": datos_ciudad.temp,
        "condicion": datos_ciudad.condicion,
        "humedad": datos_ciudad.humedad
    }
    
    return {"mensaje": "Ciudad agregada", "datos": clima_db[nombre_ciudad]}

# 5. Endpoint con Path Parameter (Para actualizar)
# URL: /actualizar-clima/madrid
@app.put("/actualizar-clima/{ciudad}", tags=["Modificaciones"])
async def actualizar_clima(ciudad: str, datos_ciudad: CiudadClima):
    """
    Actualiza el clima de una ciudad existente.
    """
    ciudad_normalizada = ciudad.lower().strip().replace(" ", "_")
    
    if ciudad_normalizada not in clima_db:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    
    clima_db[ciudad_normalizada] = {
        "temp": datos_ciudad.temp,
        "condicion": datos_ciudad.condicion,
        "humedad": datos_ciudad.humedad
    }
    
    return {"mensaje": "Ciudad actualizada", "ciudad": ciudad, "datos": clima_db[ciudad_normalizada]}

# 6. Endpoint con Path Parameter (Para eliminar)
# URL: /eliminar-clima/madrid
@app.delete("/eliminar-clima/{ciudad}", tags=["Modificaciones"])
async def eliminar_clima(ciudad: str):
    """
    Elimina una ciudad de la base de datos.
    """
    ciudad_normalizada = ciudad.lower().strip().replace(" ", "_")
    
    if ciudad_normalizada not in clima_db:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    
    del clima_db[ciudad_normalizada]
    return {"mensaje": f"Ciudad {ciudad} eliminada correctamente"}