from fastapi import FastAPI, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WeatherFast API",
    description="API rápida para obtener y gestionar datos climáticos de ciudades.",
    version="2.0.0"
    )

#=========ENDPOINTS DE LA API=========

# 0. Endpoint raíz (Información de la API)
@app.get("/", tags=["Información"])  
def root():
    """
    Endpoint raíz - Información de la API.
    """
    return {
        "api": "WeatherFast API",
        "version": "2.0.0",
        "database": "Mysql",
        "endpoints": {
            "ciudades": "/ciudades/",
            "buscar_por nombre": "/ciudades/{nombre}",
            "actualizar": "/ciudades/{ciudad_id}",
            "eliminar": "/ciudades/{ciudad_id}",
            "agregar": "/ciudades/",
            "filtar_por_condicion": "/ciudades/clima/{condicion}",
            "filtar_por_temperatura": "/ciudades/temperatura/rango" 
        }
    }

# 1. GET - Listar todas las ciudades (con paginación)
@app.get("/ciudades/", response_model=List[schemas.Ciudad], tags=["Consultas"])
def listar_ciudades(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Devuelve la lista completa de ciudades disponibles.
    """
    ciudades = db.query(models.Ciudad).offset(skip).limit(limit).all()
    return ciudades

# 2. GET - Buscar ciudad por nombre 
@app.get("/ciudades/{nombre}", response_model=schemas.Ciudad, tags=["Consultas"])
def obtener_ciudad(nombre: str, db: Session = Depends(get_db)):
    """
    Obtener datos de una ciudad específica por nombre.
    """
    ciudad = db.query(models.Ciudad).filter(models.Ciudad.nombre.ilike(f"%{nombre}%")).first()
    if not ciudad:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Ciudad '{nombre}' no encontrada")
    return ciudad

# 3. POST - Crear nueva ciudad 
@app.post("/ciudades/", response_model=schemas.Ciudad, status_code=status.HTTP_201_CREATED, tags=["Gestión"])
def crear_ciudad(ciudad: schemas.CiudadCreate, db: Session = Depends(get_db)):
    """
    Agrega una nueva ciudad a la base de datos.
    """
    try:
        nueva_ciudad = models.Ciudad(
            nombre=ciudad.nombre.lower(),
            temp=ciudad.temp,
            condicion=ciudad.condicion,
            humedad=ciudad.humedad
        )
        
        db.add(nueva_ciudad)
        db.commit()
        db.refresh(nueva_ciudad)
        
        return nueva_ciudad
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"La ciudad {ciudad.nombre} ya existe")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear la ciudad")

# 4. PUT - Actualizar ciudad existente
@app.put("/ciudades/{ciudad_id}", response_model=schemas.Ciudad, tags=["Gestión"])
def actualizar_ciudad(ciudad_id: int, datos_ciudad: schemas.CiudadUpdate, db: Session = Depends(get_db)
):
    """
    Actualiza el clima de una ciudad existente.
    """
    
    ciudad = db.query(models.Ciudad).filter(models.Ciudad.id == ciudad_id).first()
    if not ciudad:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    try:    
        ciudad.temp = datos_ciudad.temp
        ciudad.condicion = datos_ciudad.condicion
        ciudad.humedad = datos_ciudad.humedad
        
        db.commit()
        db.refresh(ciudad)
        return ciudad
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar la ciudad"
        )

# 5. Delete - Borrar una ciudad 
@app.delete("/ciudades/{ciudad_id}", tags=["Gestión"])
def eliminar_ciudad(ciudad_id: int, db: Session = Depends(get_db)):
    """
    Elimina una ciudad de la base de datos.
    """
    
    ciudad = db.query(models.Ciudad).filter(models.Ciudad.id == ciudad_id).first()
    if not ciudad:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    try:    
        nombre_ciudad = ciudad.nombre
        db.delete(ciudad)
        db.commit()
        
        return {"mensaje": f"Ciudad {nombre_ciudad} eliminada correctamente.", "id": ciudad_id }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo borrar la ciudad")

# 6. GET - Filtrar por condición climática
@app.get("/ciudades/clima/{condicion}", response_model=List[schemas.Ciudad], tags=["Consultas"])
def  filtrar_por_condicion(condicion: str, db: Session = Depends(get_db)):
    """
    Filtrar ciudades por condiccion del clima
    """
    
    ciudades =  db.query(models.Ciudad).filter(models.Ciudad.condicion.ilike(f"%{condicion}%")).all()
    
    if not ciudades:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encontraron ciudades con condición '{condicion}'")
    
    return ciudades

# 7. GET - Filtrar por rango de temperatura
@app.get("/ciudades/temperatura/rango",response_model=List[schemas.Ciudad], tags=["Consultas"])
def filtrar_por_temperatura(
    temp_min: int = 0,
    temp_max: int = 50,
    db: Session = Depends(get_db)
):
    """
    Filtrar ciudades por temperatura
    """
    
    ciudades = db.query(models.Ciudad).filter(
        models.Ciudad.temp >= temp_min,
        models.Ciudad.temp <= temp_max).all()
    
    if not ciudades:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron ciudades en el rango {temp_min}°C - {temp_max}°C")
    
    return ciudades