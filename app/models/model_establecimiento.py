from sqlmodel import SQLModel, Field

class Establecimiento(SQLModel,table = True):
    id:int|None = Field(primary_key=True)
    nombre:str = Field()
    direccion:str = Field()
    telefono:str = Field()
    email:str = Field()