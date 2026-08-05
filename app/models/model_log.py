from sqlmodel import SQLModel, Field
from datetime import datetime,timezone

class AuditLog(SQLModel,table = True):
    id:int|None = Field(primary_key=True)
    id_usuario:int = Field(foreign_key="usuario.id_usuario")
    accion:str = Field()
    detalle:str = Field()
    fecha_log:datetime = Field(default_factory=lambda: datetime.now(timezone.utc))