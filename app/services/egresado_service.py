from models.model_egresado import Egresado
from sqlmodel import Session,select
from typing import List
from sqlalchemy.orm import selectinload

from datetime import datetime
import pandas as pd

async def obtener_egresado_con_cuotas(sesion: Session, dni: int):
    
    consulta = select(Egresado).where(Egresado.dni == dni).options(selectinload(Egresado.cuotas))

    egresado_cuotas:Egresado = sesion.exec(consulta).first()

    return egresado_cuotas



async def consultar_egresados_curso(sesion:Session,id_curso:int):
    consulta = select(Egresado).where(Egresado.id_curso == id_curso)
    egresados_curso:List[Egresado] = sesion.exec(consulta).all()
    return egresados_curso 


async def estadisticas_egresado(egresado:Egresado):

    #Limpiar listado cuotas
    egresado = [e.model_dump() for e in egresado.cuotas]
    print("Egresado")
    
    df_egresado_cuotas = pd.DataFrame(egresado)

    
    print(df_egresado_cuotas)
    
    cant_cuotas_totales:int = 0
    cant_cuotas_totales = len(df_egresado_cuotas)
    cant_cuotas_impagas:int = 0
    total_no_pagado:float = float(0.00)
    cant_cuotas_pagas:int = 0
    cant_cuotas_vencidas:int = 0
    total_pagado:float = float(0.00)
    df_cuotas_pagas:pd.DataFrame = pd.DataFrame()
    df_cuotas_impagas:pd.DataFrame = pd.DataFrame()
    if len(df_egresado_cuotas)>0:
        
        df_cuotas_impagas = df_egresado_cuotas[df_egresado_cuotas['estado_pago'] == 'PENDIENTE']
        cant_cuotas_impagas = len(df_cuotas_impagas)
        total_no_pagado = df_cuotas_impagas['monto_original'].sum()

        df_cuotas_pagas = df_egresado_cuotas[df_egresado_cuotas['estado_pago'] == 'PAGADO']
        cant_cuotas_pagas = len(df_cuotas_pagas)
        total_pagado= df_cuotas_pagas['monto_original'].sum()

        fecha_actual = datetime.now()
        df_egresado_cuotas['fecha_vencimiento'] = pd.to_datetime(df_egresado_cuotas['fecha_vencimiento'])
        df_cuotas_vencidas = df_egresado_cuotas[
            (df_egresado_cuotas['estado_pago'] == 'PENDIENTE') & 
            (df_egresado_cuotas['fecha_vencimiento'] < fecha_actual)
        ]
        cant_cuotas_vencidas = len(df_cuotas_vencidas)
    
    #Calcular estado de cuenta egresado (AL DÍA, EN MORA)
    estado_cuenta:str = 'PAGOS AL DÍA'
    if cant_cuotas_vencidas > 0:
        estado_cuenta = 'EN MORA'
    elif len(df_cuotas_pagas) == 0:
        estado_cuenta = 'AL DÍA, SIN PAGOS REALIZADOS'


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


def obtener_egresado_cuotas(egresado:Egresado):

    dict_egresado:dict = [e.model_dump() for e in egresado.cuotas]
        
    print("Egresado") 
            
    df_egresado_cuotas:pd.DataFrame = pd.DataFrame(dict_egresado)

    return df_egresado_cuotas