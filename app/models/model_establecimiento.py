from sqlmodel import SQLModel, Field,Relationship
from typing import List,TYPE_CHECKING
if TYPE_CHECKING:
    from models.model_evento import Evento

class Establecimiento(SQLModel,table = True):
    id:int|None = Field(primary_key=True)
    nombre:str = Field()
    direccion:str = Field()
    telefono:str = Field()
    email:str = Field()

    #Relaciones
    eventos: List["Evento"] = Relationship(back_populates="establecimiento")