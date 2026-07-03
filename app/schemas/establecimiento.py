from models.model_establecimiento import Establecimiento

from sqlmodel import select,Session

async def obtener_establecimientos_bd(sesion:Session):
    consulta = select(Establecimiento)
    establecimientos = sesion.exec(consulta).all()
    return establecimientos