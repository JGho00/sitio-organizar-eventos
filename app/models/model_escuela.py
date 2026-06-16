from sqlmodel import Field,SQLModel


class Escuela(SQLModel , table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field()
    direccion:str= Field()
    telefono: str = Field()
    año:int = Field()



