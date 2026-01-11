from pydantic import BaseModel, Field

# Definir los esquemas Pydantic para la validación de datos
class CiudadBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50)
    temp: int = Field(..., ge=-50, le=60)
    condicion: str = Field(..., min_length=3)
    humedad: int = Field(..., ge=0, le=100)

class CiudadCreate(CiudadBase):
    pass

class CiudadUpdate(CiudadBase):
    pass

class Ciudad(CiudadBase):
    id: int
    
    class Config:
        from_attributes = True  # SQLAlchemy 2.0