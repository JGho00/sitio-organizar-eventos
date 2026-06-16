from sqlmodel import SQLModel,Field

class ItemPersona(SQLModel):
    dni:int = Field(primary_key=True)
    nombre:str
    edad:int
    nacionalidad:str

class ItemEgresado(ItemPersona):
    direccion: str
    telefono: str
    id_escuela: int
    id_curso:int
    estado_cuenta:str

class Egresado(ItemEgresado,table = True):
    pass
