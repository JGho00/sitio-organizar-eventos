from sqlmodel import SQLModel,Field,Relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.model_contrato import Contrato
    from models.model_egresado import Egresado

class Cuota(SQLModel,table = True):
    id_cuota:int = Field(primary_key=True)
    id_contrato:int = Field(foreign_key="contrato.id")
    id_egresado:int = Field(foreign_key="egresado.dni")
    numero_cuota:int = Field()
    monto_original:float = Field(default=0.00)
    monto_pago:float = Field(default=0.00)
    fecha_vencimiento:str = Field()
    estado_pago: str = Field()


    #Relacion una cuota pertenece a un egresado
    egresado: "Egresado" = Relationship(back_populates="cuotas")
    #Relacion una cuota pertenece a un contrato
    contrato: "Contrato" = Relationship(back_populates="cuotas")