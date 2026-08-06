from models.model_log import AuditLog
from sqlmodel import Session, select


async def obtener_logs(sesion:Session,username:str):

    consulta = select(AuditLog).order_by(AuditLog.fecha_log.desc())

    logs:AuditLog = sesion.exec(consulta).all()

    return logs



async def registrar_log_bd(sesion:Session,tipo_accion:str,detalle:str,usuario:int):

    nuevo_log = AuditLog(id_usuario=usuario, accion=tipo_accion, detalle=detalle)
    sesion.add(nuevo_log)
    sesion.flush()
    return nuevo_log

