from sqlmodel import Session,select
from typing import List
import pandas as pd
# servicios/cuotas.py
from sqlmodel import Session
from datetime import date
from decimal import Decimal
# dateutil es ideal para sumar meses exactos respetando los días del calendario
from dateutil.relativedelta import relativedelta
from datetime import datetime

from models.model_cuota import Cuota


async def consultar_cuotas_bd(sesion:Session):

    consulta = select(Cuota)
    cuotas:Cuota = sesion.exec(consulta).all()
    return cuotas

async def estadisticas_cuotas(cuotas:List[Cuota]):

    #Limpiar listado cuotas
    cuotas = [c.model_dump() for c in cuotas]

    df_cuotas:pd.DataFrame = pd.DataFrame(cuotas)
    print("CUOTAS", df_cuotas)
    total_cuotas:int = len(df_cuotas)
    
    total_cuotas_mes:int = 12

    #Cuotas vencidas
    #Convierto fecha_vencimiento a date
    df_cuotas['fecha_vencimiento'] = pd.to_datetime(df_cuotas['fecha_vencimiento'])
    
    fecha_actual = datetime.now()

    df_cuotas_vencidas = df_cuotas[
        (df_cuotas['estado_pago'] == 'PENDIENTE') & 
        (df_cuotas['fecha_vencimiento'] < fecha_actual)
    ]


    total_cuotas_vencidas:int = len(df_cuotas_vencidas)

    total_cuotas_pendientes:int  =len(df_cuotas[df_cuotas['estado_pago'] == 'PENDIENTE'])
    total_cuotas_finalizadas:int = len(df_cuotas[df_cuotas['estado_pago'] == 'PAGAGO'])

    estadisticas:dict = {
        'total_cuotas':total_cuotas,
        'total_cuotas_mes':total_cuotas_mes,
        'total_cuotas_vencidas': total_cuotas_vencidas,
        'total_cuotas_pendientes':total_cuotas_pendientes,
        'total_cuotas_finalizadas':total_cuotas_finalizadas,
    }

    return estadisticas

async def generar_plan_cuotas_egresado(
    id_contrato: int,
    sesion: Session, 
    monto_total_deuda: Decimal,
    egresado:int,
    dia_vencimiento: int,  # Nuevo parámetro (ej: 7)
    cantidad_cuotas: int = 12
):
    """
    Genera las cuotas distribuyendo los vencimientos exactamente 
    en el 'dia_vencimiento' de cada mes consecutivo.
    """
    # 1. Cálculos de montos y redondeos
    monto_cuota_base = (monto_total_deuda / cantidad_cuotas)
    

    # 2. Determinar el mes de inicio del plan de pagos
    hoy = date.today()
    
    for i in range(1, cantidad_cuotas + 1):
        monto_final_cuota = monto_cuota_base + (monto_cuota_base if i == 1 else 0)
        
        # Calculamos el año y mes objetivo sumando 'i' meses a la fecha actual
        mes_objetivo = hoy + relativedelta(months=i)
        
        # Intentamos fijar el día de vencimiento solicitado en el mes correspondiente.
        # relativedelta maneja automáticamente si el día excede el fin de mes 
        # (ej: si pides un día 31 y el mes es febrero, lo ajustará al 28 o 29)
        fecha_vencimiento = mes_objetivo + relativedelta(day=dia_vencimiento)

        nueva_cuota = Cuota(
            id_contrato=id_contrato,
            monto_original=monto_final_cuota,
            monto_pago=None,
            id_egresado=egresado,
            numero_cuota=i,
            fecha_vencimiento=fecha_vencimiento,
            estado_pago="PENDIENTE"
        )
        sesion.add(nueva_cuota)


    
    sesion.flush()