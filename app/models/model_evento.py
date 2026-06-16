from sqlmodel import SQLModel,Field

class Evento(SQLModel,table= True):
    id:int|None = Field(primary_key=True)
    nombre:str = Field()
    descripcion:str = Field()
    id_curso:int = Field()
    fecha_evento:str = Field()
    salon_lugar:str = Field()
    estado : str = Field()