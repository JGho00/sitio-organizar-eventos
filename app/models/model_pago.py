from sqlmodel import SQLModel,Field,Relationship
from datetime import datetime,timezone
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    
    from models.model_cuota import Cuota

class Pago(SQLModel,table = True):
    id_pago:int = Field(primary_key=True)
    id_cuota:int = Field(foreign_key="cuota.id_cuota",ondelete="CASCADE")
    fecha:datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    monto:float = Field()
    metodo_pago:str = Field()
    ruta_comprobante:str|None = Field(default=None)
    cobrador:str = Field()

    #Relaciones
    cuota: "Cuota" = Relationship(back_populates="pagos")