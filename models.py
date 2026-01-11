from sqlalchemy import Column, Integer, String
from database import Base

#Crear tablas en la base de datos
#Crear el modelo de la base de datos para las ciudades
class Ciudad(Base):
    __tablename__ = "ciudades"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, index=True, nullable=False)
    temp = Column(Integer, nullable=False)
    condicion = Column(String(50), nullable=False)
    humedad = Column(Integer, nullable=False)