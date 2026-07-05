from sqlmodel import Session,select

from models.model_contrato import Contrato



async def obtener_contratos_bd(sesion:Session):

    consulta = select(Contrato)

    resultado = sesion.exec(consulta)

    contratos = resultado.all()

    return contratos

async def crear_contrato_bd(sesion:Session,contrato:Contrato):
    sesion.add(contrato)
    #sesion.commit()
    #sesion.refresh(contrato)
    sesion.flush()
    return contrato


async def obtener_estadisticas_contratos_bd(sesion:Session):
    consulta = select(Contrato)
    resultado = sesion.exec(consulta)
    
    contratos:Contrato = resultado.all()

    total_contratos = len(contratos)

    total_contratos_activos = len([contrato for contrato in contratos if contrato.fecha_fin == None])
    total_contratos_finalizados = len([contrato for contrato in contratos if contrato.fecha_fin != None])
    total_monto = sum([contrato.monto_total for contrato in contratos])
    promedio_monto = total_monto / total_contratos if total_contratos > 0 else 0
    return {
        "total_contratos": total_contratos,
        "total_contratos_activos": total_contratos_activos,
        "total_contratos_finalizados": total_contratos_finalizados,
        "total_monto": total_monto,
        "promedio_monto": promedio_monto
    }