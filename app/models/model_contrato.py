from sqlmodel import SQLModel,Field
from datetime import datetime,timezone

class Contrato(SQLModel,table=True):
    id:int = Field(primary_key=True)
    nombre:str = Field()
    id_egresado:int = Field()
    fecha_inicio:datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    fecha_fin:datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    monto_total:float = Field()
    cantidad_de_cuotas:int = Field()
    interes_mora:float = Field()
    dia_vencimiento_mensual:str = Field()