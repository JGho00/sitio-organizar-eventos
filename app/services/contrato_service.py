from sqlmodel import Session,select

from models.model_contrato import Contrato
from models.model_curso import Curso
from models.model_evento import Evento
from models.model_egresado import Egresado
from models.model_cuota import Cuota
from models.model_pago import Pago



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

    #Eliminación explícita por pasos, sin depender del cascade de la base de datos.

    #1. Identificar curso y evento asociados al contrato
    curso:Curso = sesion.get(Curso, contrato.id_curso)
    evento:Evento = sesion.get(Evento, contrato.id_evento)

    #2. Identificar egresados del curso
    egresados = sesion.exec(
        select(Egresado).where(Egresado.id_curso == curso.id)
    ).all()

    #3. Identificar y eliminar cuotas y pagos de cada egresado
    for egresado in egresados:
        cuotas = sesion.exec(
            select(Cuota).where(Cuota.id_egresado == egresado.dni)
        ).all()

        for cuota in cuotas:
            pagos = sesion.exec(
                select(Pago).where(Pago.id_cuota == cuota.id_cuota)
            ).all()

            for pago in pagos:
                sesion.delete(pago)

            sesion.delete(cuota)

        #4. Eliminar el egresado
        sesion.delete(egresado)

    #5. Eliminar el contrato (debe ir antes que curso y evento, ya que los referencia)
    sesion.delete(contrato)

    #6. Eliminar el evento asociado al curso
    if evento:
        sesion.delete(evento)

    #7. Eliminar el curso (la escuela no se toca, es el padre del curso)
    sesion.delete(curso)

    sesion.flush()

    return contrato

async def estadisticas_contratos(sesion:Session,contratos:Contrato):
    


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