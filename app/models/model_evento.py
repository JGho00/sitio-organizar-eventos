from sqlmodel import SQLModel,Field,Relationship
from typing import Optional
from datetime import datetime

from models.model_establecimiento import Establecimiento

class Evento(SQLModel,table= True):
    id:int|None = Field(primary_key=True)
    nombre:str = Field()
    descripcion:str = Field()
    id_curso:int = Field(foreign_key="curso.id")
    fecha_evento:Optional[datetime | None] = Field(default=None)
    id_establecimiento:int = Field(foreign_key="establecimiento.id")
    estado : str = Field()

    #Relaciones
    establecimiento: "Establecimiento" = Relationship(back_populates="eventos")