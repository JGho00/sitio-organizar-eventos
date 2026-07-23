from sqlmodel import SQLModel,Field, Relationship
from typing import TYPE_CHECKING
from sqlalchemy import asc,text


if TYPE_CHECKING:
    from models.model_curso import Curso
    from models.model_cuota import Cuota
    from models.model_escuela import Escuela

class Persona(SQLModel):
    dni:int = Field(primary_key=True)
    nombre:str = Field()
    direccion:str = Field()
    edad:str = Field()
    telefono: str

class Egresado(Persona,table = True):
    id_curso:int =Field(default=None, foreign_key="curso.id",ondelete="CASCADE")

    #Relaciones
    curso: "Curso" = Relationship(back_populates="egresados")


    cuotas: list["Cuota"] = Relationship(
        back_populates="egresado",
        sa_relationship_kwargs={
            # Queda explícito que va de menor a mayor
           "order_by": "Cuota.numero_cuota",
           "passive_deletes": True
        }
    )