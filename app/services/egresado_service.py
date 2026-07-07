from models.model_egresado import Egresado
from sqlmodel import Session,select
from typing import List
from sqlalchemy.orm import selectinload

from datetime import datetime
import pandas as pd

async def obtener_egresado_con_cuotas(sesion: Session, dni: int):
    # Usamos selectinload para forzar la carga de la relación 'cuotas'
    consulta = select(Egresado).where(Egresado.dni == dni).options(selectinload(Egresado.cuotas))
    egresado_cuotas:Egresado = sesion.exec(consulta).first()
    return egresado_cuotas


async def estadisticas_egresado_generales(egresados:List[Egresado]):
    pass
    

    


async def estadisticas_egresado(egresado:Egresado):

    #Limpiar listado cuotas
    egresado = [e.model_dump() for e in egresado.cuotas]

    df_egresado_cuotas = pd.DataFrame(egresado)

    cant_cuotas_totales = len(df_egresado_cuotas)

    
    
    df_cuotas_impagas:pd.DataFrame = df_egresado_cuotas[df_egresado_cuotas['estado_pago'] == 'PENDIENTE']
    cant_cuotas_impagas:int = len(df_cuotas_impagas)
    total_no_pagado:float = df_cuotas_impagas['monto_original'].sum()

    df_cuotas_pagas:pd.DataFrame = df_egresado_cuotas[df_egresado_cuotas['estado_pago'] == 'PAGADO']
    cant_cuotas_pagas:int = len(df_cuotas_pagas)
    total_pagado:float = df_cuotas_pagas['monto_original'].sum()

    fecha_actual = datetime.now()
    df_egresado_cuotas['fecha_vencimiento'] = pd.to_datetime(df_egresado_cuotas['fecha_vencimiento'])
    df_cuotas_vencidas = df_egresado_cuotas[
        (df_egresado_cuotas['estado_pago'] == 'PENDIENTE') & 
        (df_egresado_cuotas['fecha_vencimiento'] < fecha_actual)
    ]
    cant_cuotas_vencidas:int = len(df_cuotas_vencidas)
    
    #Calcular estado de cuenta egresado (AL DÍA, EN MORA)
    estado_cuenta:str = 'AL DÍA'
    if cant_cuotas_vencidas > 0:
        estado_cuenta = 'EN MORA'


    estadisticas:dict = {
        'cant_cuotas_totales': cant_cuotas_totales,
        'cant_cuotas_pagas': cant_cuotas_pagas,
        'cant_cuotas_impagas': cant_cuotas_impagas,
        'total_pagado': total_pagado,
        'total_no_pagado':total_no_pagado,
        'cant_cuotas_vencidas': cant_cuotas_vencidas,
        'estado_cuenta': estado_cuenta
    }

    return estadisticas