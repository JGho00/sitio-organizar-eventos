from sqlmodel import SQLModel,Session,select

from models.model_contrato import Contrato

from core.config import obtener_sesion


async def obtener_contratos_bd(sesion:Session):

    consulta = select(Contrato)

    resultado = sesion.exec(consulta)

    contratos = resultado.all()

    return contratos