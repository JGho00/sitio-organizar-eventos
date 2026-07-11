from sqlmodel import SQLModel,Field,Relationship
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.model_contrato import Contrato
    from models.model_egresado import Egresado
    from models.model_pago import Pago

class Cuota(SQLModel,table = True):
    id_cuota:int = Field(primary_key=True)
    id_contrato:int = Field(foreign_key="contrato.id",ondelete="CASCADE")
    id_egresado:int = Field(foreign_key="egresado.dni",ondelete="CASCADE")
    numero_cuota:int = Field()
    monto_original:Decimal = Field(default=0.00,decimal_places=2)
    monto_pago:Decimal = Field(default=0.00,decimal_places=2)
    fecha_vencimiento:str = Field()
    estado_pago: str = Field()


    #Relacion una cuota pertenece a un egresado
    egresado: "Egresado" = Relationship(back_populates="cuotas")
    #Relacion una cuota pertenece a un contrato
    contrato: "Contrato" = Relationship(back_populates="cuotas")
    pagos: list["Pago"] = Relationship(back_populates="cuota")