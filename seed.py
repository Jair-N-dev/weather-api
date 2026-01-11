from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# Crear tablas
models.Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    # Verificar si ya hay datos
    if db.query(models.Ciudad).first():
        print("La base de datos ya tiene datos")
        return
    
    # Datos iniciales
    ciudades_iniciales = [
        {"nombre": "madrid", "temp": 25, "condicion": "Soleado", "humedad": 40},
        {"nombre": "bogota", "temp": 18, "condicion": "Nublado", "humedad": 70},
        {"nombre": "mexico", "temp": 22, "condicion": "Despejado", "humedad": 30},
        {"nombre": "buenos_aires", "temp": 20, "condicion": "Lluvia", "humedad": 85},
        {"nombre": "barranquilla", "temp": 32, "condicion": "Soleado", "humedad": 75}
    ]
    
    for ciudad_data in ciudades_iniciales:
        ciudad = models.Ciudad(**ciudad_data)
        db.add(ciudad)
    
    db.commit()
    print(f"✅ {len(ciudades_iniciales)} ciudades agregadas exitosamente")
    db.close()

if __name__ == "__main__":
    seed_database()