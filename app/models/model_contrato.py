from sqlmodel import SQLModel,Field
from datetime import datetime
class Contrato(SQLModel,table=True):
    id:int = Field(primary_key=True)
    nombre:str = Field()
    id_curso:int = Field()
    monto_total:float = Field()
    monto_total_por_egresado:float = Field()
    interes_mora:float = Field()
    dia_vencimiento_mensual:str = Field()