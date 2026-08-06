from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime,timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.model_usuario import Usuario

class AuditLog(SQLModel,table = True):
    id:int|None = Field(primary_key=True)
    id_usuario:int = Field(foreign_key="usuario.id_usuario")
    accion:str = Field()
    detalle:str = Field()
    fecha_log:datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    #Relacion un log pertenece a un usuario
    usuario: "Usuario" = Relationship()