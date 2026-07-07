from sqlmodel import Session

from services.egresado_service import estadisticas_egresado
from services.contrato_service import estadisticas_contratos
from services.cuota_service import consultar_cuotas_bd,estadisticas_cuotas
from services.evento_service import estadisticas_eventos


async def obtener_estadisticas_generales(sesion:Session):

    resumen_contratos = await estadisticas_contratos(sesion)

    #resumen_egresados = await estadisticas_egresado(sesion)

    resumen_cuotas = await estadisticas_cuotas(sesion)
    print("RESUMEN Cuotas",resumen_cuotas)

    resumen_eventos = await estadisticas_eventos(sesion)

    estadisticas_globales:dict = {

        'contratos': resumen_contratos,
        #'egresados': resumen_egresados,
        'cuotas':resumen_cuotas,
        'eventos':resumen_eventos
    }

    return estadisticas_globales