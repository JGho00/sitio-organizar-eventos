from sqlmodel import SQLModel,Field

class Persona(SQLModel):
    dni:int = Field(primary_key=True)
    nombre:str = Field()
    direccion:str = Field()
    edad:str = Field()

class Egresado(Persona,table = True):
    telefono: str
    id_escuela: int
    id_curso:int
    estado_cuenta:str

#e = Egresado(dni=2,nombre='jose',direcion  = 'santa fe 1299',telefono='222',id_curso=1,id_escuela = 1,estado_cuenta='AL DIA')
