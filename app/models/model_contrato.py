from sqlmodel import SQLModel,Field,Relationship
from datetime import datetime,timezone
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from models.model_curso import Curso
    from models.model_cuota import Cuota

class Contrato(SQLModel,table=True):
    id:int = Field(primary_key=True,default=None)
    id_evento:int = Field(foreign_key="evento.id")
    id_curso:int = Field(foreign_key="curso.id")
    fecha_inicio:datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    fecha_fin:Optional[datetime] = Field(default=None)
    monto_total:float = Field()
    interes_mora:float = Field()
    dia_vencimiento_mensual:str = Field()


    # Relación: Un contrato pertenece a un curso
    curso: "Curso" = Relationship(back_populates="contratos")
    #Relacion un contrato puede tener varias cuotas
    cuotas: list["Cuota"] = Relationship(back_populates="contrato")