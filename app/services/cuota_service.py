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
from models.model_curso import Curso
from models.model_escuela import Escuela
from models.model_pago import Pago
from services.dependencias import obtener_fecha


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
        Egresado.nombre.label("nombre_egresado"),  # Traemos el nombre desde Egresado
        Egresado.id_curso,
        Curso.id.label("curso_id"),
        Curso.id_escuela,
        Escuela.id.label("escuela_id"),
        Escuela.nombre.label("escuela_nombre")
    ).join(Egresado, Cuota.id_egresado == Egresado.dni).join(Curso,Curso.id == Egresado.id_curso).join(Escuela,Escuela.id == Curso.id_escuela)

    cuotas:Cuota = sesion.exec(consulta).all()
    
    df_cuotas = pd.DataFrame([r._asdict() for r in cuotas])
    
    return df_cuotas

async def consultar_cuota_id_bd(sesion:Session,id_cuota:int):

    consulta = select(Cuota).where(Cuota.id_cuota == id_cuota)

    cuota:Cuota = sesion.exec(consulta).first()
    
    return cuota
    
async def actualizar_cuota_bd(sesion:Session,cuota:Cuota,monto_pago:Decimal):

    #Acumulo pagos de la cuota.
    #Nota: cuota.monto_pago puede venir en None para cuotas generadas antes de la
    #corrección en generar_plan_cuotas_egresado (ver comentario allí). Si no se contempla
    #este caso, "None + Decimal" lanza TypeError y el pago se pierde (se revierte la
    #transacción completa en registrar_pago_cuota), por eso la cuota nunca sale de
    #PENDIENTE y los montos del dashboard (cobrado del mes, morosidad) quedan mal.
    monto_pago_actual = cuota.monto_pago if cuota.monto_pago is not None else Decimal('0.00')
    monto_acumulado = monto_pago_actual + monto_pago
    cuota.monto_pago = monto_acumulado
    
    #Restar monto original - monto del pago
    monto_actualizado = Decimal(cuota.monto_original) - monto_acumulado

    
    if int(monto_actualizado) == 0:
        cuota.estado_pago = 'PAGADO'
    
    sesion.add(cuota)
    sesion.flush()

    return cuota


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

async def consultar_monto_pagado_periodo(sesion:Session,periodo:str = None):
    '''
        Suma el monto de los pagos (tabla Pago) cuya fecha real de pago cae dentro
        del período "MM-YYYY" indicado (o el mes actual si no se especifica).
    '''
    if not periodo:
        fechas:dict = obtener_fecha()
        periodo:str = fechas['mm_yyyy'].replace('_','-')

    consulta = select(Pago.monto,Pago.fecha)
    pagos = sesion.exec(consulta).all()

    if not pagos:
        return Decimal('0.00')

    df_pagos = pd.DataFrame([r._asdict() for r in pagos])
    df_pagos['fecha'] = pd.to_datetime(df_pagos['fecha'])

    df_pagos_periodo = df_pagos[df_pagos['fecha'].dt.to_period('M') == periodo]

    return df_pagos_periodo['monto'].sum() if not df_pagos_periodo.empty else Decimal('0.00')

async def estadisticas_cuotas(sesion:Session):

    df_cuotas:pd.DataFrame = await consultar_cuotas_bd(sesion)

    if len(df_cuotas) == 0:
        estadisticas:dict= {}
        return estadisticas
    

    total_cuotas:int = len(df_cuotas)
    
    df_cuotas_mes:pd.DataFrame = consultar_cuotas_por_periodo(df_cuotas)
    total_cuotas_mes:int = len(df_cuotas_mes)
    total_proyeccion_mes = df_cuotas_mes['monto_original'].sum()
    

    df_cuotas_vencidas = consultar_cuotas_vencidas(df_cuotas)
    cant_cuotas_vencidas:int = len(consultar_cuotas_vencidas(df_cuotas))
    monto_total_vencidas:float = df_cuotas_vencidas['monto_original'].sum()

    #Ingresos del mes.
    #Antes se sumaba "monto_pago" de las cuotas cuyo VENCIMIENTO caía en el mes actual
    #y que ya estaban en estado PAGADO. Eso era incorrecto porque: (a) un pago puede
    #haberse realizado en un mes distinto al de vencimiento de la cuota, y (b) los pagos
    #parciales (cuota aún PENDIENTE pero con algo abonado) quedaban afuera del total.
    #Ahora se calcula sobre la FECHA REAL del pago (tabla Pago), que es la fuente de
    #verdad de "cuánto se cobró" en el mes.
    monto_mes_pagado = await consultar_monto_pagado_periodo(sesion)

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

        # monto_pago se inicializa en 0.00 (no en None): el modelo Cuota lo define como
        # Decimal no-opcional, pero al ser una tabla SQLModel no valida el tipo en runtime,
        # por lo que pasar None se guardaba igual como NULL en la base. Eso rompía
        # actualizar_cuota_bd en el primer pago de cada cuota ("None + Decimal" -> TypeError),
        # el cual además hacía rollback de toda la transacción (incluido el pago ya creado).
        # Como consecuencia, ninguna cuota lograba pasar a PAGADO y los montos del dashboard
        # ("cobrado este mes" y "morosidad total") quedaban mal calculados.
        nueva_cuota = Cuota(
            id_contrato=id_contrato,
            monto_original=monto_cuota_base,
            monto_pago=Decimal('0.00'),
            id_egresado=egresado,
            numero_cuota=i,
            fecha_vencimiento=fecha_vencimiento,
            estado_pago="PENDIENTE"
        )
        sesion.add(nueva_cuota)


    
    sesion.flush()