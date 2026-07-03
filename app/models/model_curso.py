from sqlmodel import SQLModel, Field,Relationship
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.model_escuela import Escuela
    from models.model_contrato import Contrato
    


class Curso(SQLModel,table = True):
    id:int = Field(primary_key=True,default=None)
    id_escuela:int = Field(default=None,foreign_key="escuela.id")
    division:str = Field()
    año:int = Field()

    # Relaciones
    escuela: "Escuela" = Relationship(back_populates="cursos")
    contratos: List["Contrato"] = Relationship(back_populates="curso")