from models.model_log import AuditLog
from sqlmodel import Session, select


async def obtener_logs(sesion:Session,username:str):

    consulta = select(AuditLog).order_by(AuditLog.fecha_log.desc())

    logs:AuditLog = sesion.exec(consulta).all()

    return logs
