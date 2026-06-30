from sqlmodel import SQLModel,Field

class Cuota(SQLModel,table = True):
    id_cuota:int = Field(primary_key=True)
    id_contrato:int = Field(foreign_key="contrato.id")
    numero_cuota:int = Field()
    monto_original:float = Field()
    monto_retrasado:float = Field()
    fecha_vencimiento:str = Field()
    estado_pago: str = Field()