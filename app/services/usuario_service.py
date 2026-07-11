from models.model_usuario import Usuario

from sqlmodel import Session, select


async def obtener_usuario_activo_bd(sesion:Session,username:str):

    consulta = select(Usuario).where(Usuario.username == username)

    resultado = sesion.exec(consulta)

    usuario:Usuario = resultado.first()

    return usuario
