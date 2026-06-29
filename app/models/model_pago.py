from sqlmodel import SQLModel,Field
from datetime import datetime,timezone

class Pago(SQLModel,table = True):
    id_pago:int = Field(primary_key=True)
    id_cuota:int = Field(foreign_key="cuota.id_cuota")
    fecha:datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    monto:float = Field()
    metodo_pago:str = Field()
    nro_comprobante:str = Field()
    cobrador:str = Field()