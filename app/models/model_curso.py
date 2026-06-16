from sqlmodel import SQLModel, Field

class Curso(SQLModel,table = True):
    id:int = Field(primary_key=True)
    id_escuela:int = Field()
    division:str = Field()
    año:int = Field()
    cantidad_egresados:int = Field()