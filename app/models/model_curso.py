from sqlmodel import SQLModel, Field

class Curso(SQLModel,table = True):
    id:int = Field(primary_key=True)
    id_escuela:int = Field(default=None,foreign_key="escuela.id")
    division:str = Field()
    año:int = Field()