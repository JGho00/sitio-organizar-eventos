from sqlmodel import Field,SQLModel,Session

class Escuela(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field()
    direccion:str= Field()
    telefono: str = Field()
    año:int = Field()


    

#escuela_1 = Escuela(nombre = 'Colegio 1',direccion='calle',telefono='4444',año=2027)
#escuela_2 = Escuela(nombre = 'Colegio 2',direccion='calle',telefono='4444',año=2027)
#escuela_3 = Escuela(nombre = 'Colegio 3',direccion='calle',telefono='4444',año=2027)


#SQLModel.metadata.create_all(engine)

#with Session(engine) as bd_sesion:
#    bd_sesion.add(escuela_1)
#    bd_sesion.add(escuela_2)
#    bd_sesion.add(escuela_3)


#   bd_sesion.commit() 
