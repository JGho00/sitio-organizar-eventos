from sqlmodel import Session,select
from typing import List
import pandas as pd
from sqlmodel import Session
from datetime import date
from decimal import Decimal,ROUND_CEILING
from dateutil.relativedelta import relativedelta
from datetime import datetime

from models.model_cuota import Cuota
from models.model_egresado import Egresado
from services.dependencias import obtener_fecha
from services.pago_service import consultar_pagos_bd


async def consultar_cuotas_bd(sesion:Session):

    consulta = select(
        Cuota.id_cuota,
        Cuota.id_egresado,
        Cuota.fecha_vencimiento,
        Cuota.numero_cuota,
        Cuota.monto_original,
        Cuota.monto_pago,
        Cuota.estado_pago,
        Cuota.fecha_vencimiento,
        # Agrega aquí todos los campos de Cuota que necesites...
        Egresado.nombre.label("nombre_egresado")  # Traemos el nombre desde Egresado
    ).join(Egresado, Cuota.id_egresado == Egresado.dni)

    cuotas:Cuota = sesion.exec(consulta).all()
    
    df_cuotas = pd.DataFrame([r._asdict() for r in cuotas])
    
    return df_cuotas

async def consultar_cuota_id_bd(sesion:Session,id_cuota:int):

    consulta = select(Cuota).where(Cuota.id_cuota == id_cuota)

    cuota:Cuota = sesion.exec(consulta).first()
    
    return cuota
    
async def actualizar_cuota_bd(sesion:Session,cuota:Cuota,monto_pago:Decimal):
    #Restar monto original - monto del pago
    monto_actualizado = Decimal(cuota.monto_original) - monto_pago

    print("MONNTO ACTUALIZADO",monto_actualizado)
    cuota.monto_original = monto_actualizado
    cuota.monto_pago = monto_pago
    if int(monto_actualizado) == 0:
        cuota.estado_pago = 'PAGADO'
    
    sesion.add(cuota)
    sesion.flush()


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

    df_cuotas_vencidas = df_cuotas_vencidas.sort_values(by=['fecha_vencimiento', 'monto_original'], ascending=False)
    
    return df_cuotas_vencidas

def consultar_proximos_vencimientos(df_cuotas:pd.DataFrame):
   
    #Convertir la columna fecha a datetime
    df_cuotas['fecha_vencimiento'] = pd.to_datetime(df_cuotas['fecha_vencimiento'])

    #Se filtra por fecha de vencimiento más cercana. Se ordena por fecha. Se obtiene solo los primeros 10 registros
    hoy:pd.Timestamp = pd.Timestamp.today().normalize()
    proximos_15_dias:pd.Timestamp = hoy + pd.Timedelta(days=15)

    # 3. Filtrar los registros dentro del rango
    vencimientos_15_dias:pd.DataFrame = df_cuotas[
        (df_cuotas['estado_pago']=='PENDIENTE')&
        (df_cuotas['fecha_vencimiento'] >= hoy) & 
        (df_cuotas['fecha_vencimiento'] <= proximos_15_dias)
    ].sort_values(by='fecha_vencimiento')
        
    print("PROXIMOS VENCIMIENTOS")
    print(vencimientos_15_dias)
    return vencimientos_15_dias.to_dict(orient='records')

async def estadisticas_cuotas(sesion:Session):

    df_cuotas:pd.DataFrame = await consultar_cuotas_bd(sesion)

    

    total_cuotas:int = len(df_cuotas)
    
    df_cuotas_mes:pd.DataFrame = consultar_cuotas_por_periodo(df_cuotas)
    total_cuotas_mes:int = len(df_cuotas_mes)
    total_proyeccion_mes = df_cuotas_mes['monto_original'].sum()
    

    df_cuotas_vencidas = consultar_cuotas_vencidas(df_cuotas)
    cant_cuotas_vencidas:int = len(consultar_cuotas_vencidas(df_cuotas))
    monto_total_vencidas:float = df_cuotas_vencidas['monto_original'].sum()

    #Ingresos
    df_cuotas_pagas_mes:pd.DataFrame = consultar_cuotas_por_estado_pago(df_cuotas_mes)
    
    monto_mes_pagado = (df_cuotas_pagas_mes['monto_pago'].sum())
    print("total",monto_mes_pagado)

    cant_cuotas_pendientes:int  =len(df_cuotas[df_cuotas['estado_pago'] == 'PENDIENTE'])
    print("PENDIENTES")
    print(cant_cuotas_pendientes)
    cant_cuotas_finalizadas:int = len(df_cuotas[df_cuotas['estado_pago'] == 'PAGADO'])


    #Proximos vencimientos del mes
    proximos_vencimientos:dict = consultar_proximos_vencimientos(df_cuotas)
    
    estadisticas:dict = {
        'total_cuotas':total_cuotas,
        'total_cuotas_mes':total_cuotas_mes,
        'total_proyeccion_mes':total_proyeccion_mes,
        'cant_cuotas_vencidas': cant_cuotas_vencidas,
        'total_cuotas_pagas_mes':'',
        'total_cuotas_impagas_mes':'',
        'cant_cuotas_pendientes':cant_cuotas_pendientes,
        'cant_cuotas_finalizadas':cant_cuotas_finalizadas,
        'monto_mes_pagado':monto_mes_pagado,
        'monto_total_morosidad': monto_total_vencidas,
        'proximos_vencimientos': proximos_vencimientos
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
    monto_cuota_base:Decimal = (monto_total_deuda / cantidad_cuotas)
    monto_cuota_base = monto_cuota_base.quantize(Decimal('0.01'),rounding = ROUND_CEILING)

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