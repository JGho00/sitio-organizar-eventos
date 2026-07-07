from sqlmodel import Session,select
from typing import List
import pandas as pd
from sqlmodel import Session
from datetime import date
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from datetime import datetime

from models.model_cuota import Cuota

from services.dependencias import obtener_fecha


async def consultar_cuotas_bd(sesion:Session):

    consulta = select(Cuota)
    cuotas:Cuota = sesion.exec(consulta).all()

    #Convertir los objetos SQLModel a diccionarios
    cuotas_dict = [cuota.model_dump() for cuota in cuotas]
    
    #Crear y retornar el DataFrame
    df_cuotas = pd.DataFrame(cuotas_dict)
    return df_cuotas

def consultar_cuotas_por_periodo(df_cuotas:pd.DataFrame,periodo:str = None):
    '''
        Función que busca cuotas por periodo en formato "MM-YYYY"
    '''
    df_cuotas["fecha_vencimiento"] = pd.to_datetime(df_cuotas["fecha_vencimiento"])

    if not periodo:
        fechas:dict = obtener_fecha()
        periodo:str = fechas['mm_yyyy'].replace('_','-')

    # 2. Definir el mes/año y el estado que buscas
    mes_buscado = periodo

    # 3. Filtrar por mes y por estado al mismo tiempo
    df_cuotas = df_cuotas[
        (df_cuotas["fecha_vencimiento"].dt.to_period("M") == mes_buscado)
    ]

    return df_cuotas

def consultar_cuotas_por_estado_pago(df_cuotas:pd.DataFrame,estado:str = 'PAGADO'):
    
    
    df_cuotas = df_cuotas[
        (df_cuotas["estado_pago"] == estado)
    ]

    return df_cuotas

def consultar_cuotas_vencidas(df_cuotas:pd.DataFrame):
    fecha_actual = datetime.now()
    #Cuotas vencidas
    #Convierto fecha_vencimiento a date
    df_cuotas['fecha_vencimiento'] = pd.to_datetime(df_cuotas['fecha_vencimiento'])
    
    df_cuotas_vencidas = df_cuotas[
        (df_cuotas['estado_pago'] == 'PENDIENTE') & 
        (df_cuotas['fecha_vencimiento'] < fecha_actual)
    ]

    return df_cuotas_vencidas

async def estadisticas_cuotas(sesion:Session):

    df_cuotas:pd.DataFrame = await consultar_cuotas_bd(sesion)

    

    total_cuotas:int = len(df_cuotas)
    
    df_cuotas_mes:pd.DataFrame = consultar_cuotas_por_periodo(df_cuotas)
    total_cuotas_mes:int = len(df_cuotas_mes)
    total_proyeccion_mes = df_cuotas_mes['monto_original'].sum()
    


    total_cuotas_vencidas:int = len(consultar_cuotas_vencidas(df_cuotas))


    #Ingresos
    df_cuotas_pagas_mes:pd.DataFrame = consultar_cuotas_por_estado_pago(df_cuotas_mes)
    
    monto_mes_pagado = (df_cuotas_pagas_mes['monto_pago'].sum())
    print("total",monto_mes_pagado)

    total_cuotas_pendientes:int  =len(df_cuotas[df_cuotas['estado_pago'] == 'PENDIENTE'])
    total_cuotas_finalizadas:int = len(df_cuotas[df_cuotas['estado_pago'] == 'PAGADO'])

    estadisticas:dict = {
        'total_cuotas':total_cuotas,
        'total_cuotas_mes':total_cuotas_mes,
        'total_proyeccion_mes':total_proyeccion_mes,
        'total_cuotas_vencidas': total_cuotas_vencidas,
        'total_cuotas_pagas_mes':'',
        'total_cuotas_impagas_mes':'',
        'total_cuotas_pendientes':total_cuotas_pendientes,
        'total_cuotas_finalizadas':total_cuotas_finalizadas,
        'monto_mes_pagado':monto_mes_pagado
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
        
        
        # Calculamos el año y mes objetivo sumando 'i' meses a la fecha actual
        mes_objetivo = hoy + relativedelta(months=i)
        
        # Intentamos fijar el día de vencimiento solicitado en el mes correspondiente.
        # relativedelta maneja automáticamente si el día excede el fin de mes 
        # (ej: si pides un día 31 y el mes es febrero, lo ajustará al 28 o 29)
        fecha_vencimiento = mes_objetivo + relativedelta(day=dia_vencimiento)

        nueva_cuota = Cuota(
            id_contrato=id_contrato,
            monto_original=monto_cuota_base,
            monto_pago=None,
            id_egresado=egresado,
            numero_cuota=i,
            fecha_vencimiento=fecha_vencimiento,
            estado_pago="PENDIENTE"
        )
        sesion.add(nueva_cuota)


    
    sesion.flush()