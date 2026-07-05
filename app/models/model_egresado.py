from sqlmodel import SQLModel,Field, Relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.model_curso import Curso
    from models.model_cuota import Cuota

class Persona(SQLModel):
    dni:int = Field(primary_key=True)
    nombre:str = Field()
    direccion:str = Field()
    edad:str = Field()
    telefono: str

class Egresado(Persona,table = True):
    id_curso:int =Field(default=None, foreign_key="curso.id")

    #Relaciones
    curso: "Curso" = Relationship(back_populates="egresados")

    cuotas: list["Cuota"] = Relationship(back_populates="egresado")