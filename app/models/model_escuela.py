from sqlmodel import Field,SQLModel,select
from typing import List,TYPE_CHECKING
from sqlmodel import Relationship

if TYPE_CHECKING:
    from .model_curso import Curso 

class Escuela(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field()
    direccion:str= Field()
    telefono: str = Field()

    cursos: List["Curso"] = Relationship(back_populates="escuela")

