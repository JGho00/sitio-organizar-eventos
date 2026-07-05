from sqlmodel import SQLModel, Field,Relationship
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.model_escuela import Escuela
    from models.model_contrato import Contrato
    from models.model_egresado import Egresado


class Curso(SQLModel,table = True):
    id:int = Field(primary_key=True,default=None)
    id_escuela:int = Field(foreign_key="escuela.id")
    division:str = Field()
    año:int = Field()

    #Relacion un curso pertenece a una escuela, una escuela puede tener varios cursos
    escuela: "Escuela" = Relationship(back_populates="cursos")

    #Relacion un curso puede tener varios contratos (en general el 1 pero puede tener 2 en caso de actualización de montos)
    contratos: List["Contrato"] = Relationship(back_populates="curso")

    #Relacion un curso puede tener varios egresados
    egresados: List["Egresado"] = Relationship(back_populates="curso")