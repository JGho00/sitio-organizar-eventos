from sqlmodel import Session,select
from typing import List
from models.model_evento import Evento

async def obtener_eventos(sesion:Session):
    consulta = select(Evento)
    eventos:Evento = sesion.exec(consulta).all()
    return eventos

async def estadisticas_eventos(eventos:List[Evento]):
    
    pass