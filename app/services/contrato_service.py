from sqlmodel import Session,select

from models.model_contrato import Contrato



async def obtener_contratos_bd(sesion:Session):

    consulta = select(Contrato)

    resultado = sesion.exec(consulta)

    contratos = resultado.all()

    return contratos

async def obtener_contrato_id_bd(sesion:Session,id:int):

    consulta = select(Contrato).where(Contrato.id == id)

    resultado = sesion.exec(consulta)

    contrato:Contrato = resultado.first()

    return contrato

async def crear_contrato_bd(sesion:Session,contrato:Contrato):
    sesion.add(contrato)
    #sesion.commit()
    #sesion.refresh(contrato)
    sesion.flush()
    return contrato

async def eliminar_contrato_bd(sesion:Session,contrato:Contrato):
    


    sesion.delete(contrato)
    #sesion.commit()
    sesion.flush()
    
    return contrato


async def estadisticas_contratos(sesion:Session):
    
    
    contratos:Contrato = await obtener_contratos_bd(sesion)

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