from sqlmodel import Session

from services.egresado_service import estadisticas_egresado
from services.contrato_service import estadisticas_contratos
from services.cuota_service import estadisticas_cuotas
from services.evento_service import estadisticas_eventos

async def obtener_estadisticas_generales(sesion:Session):

    resumen_contratos = await estadisticas_contratos(sesion)

    estadisticas_globales:dict = {

        'contratos': resumen_contratos,
        
    }

    return estadisticas_globales