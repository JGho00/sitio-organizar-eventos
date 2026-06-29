from sqlmodel import SQLModel,Field
class Persona(SQLModel):
    dni:int = Field(primary_key=True)
    nombre:str = Field()
    direccion:str = Field()
    edad:str = Field()
    telefono: str

class Egresado(Persona,table = True):
    id_curso:int =Field(default=None, foreign_key="curso.id")

