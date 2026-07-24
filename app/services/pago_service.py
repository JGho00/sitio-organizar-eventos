from sqlmodel import Session,select
from typing import List
import pandas as pd
from sqlmodel import Session
from datetime import date
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from datetime import datetime

from models.model_cuota import Cuota
from models.model_egresado import Egresado
from models.model_pago import Pago
from models.model_curso import Curso
from models.model_escuela import Escuela
from services.dependencias import obtener_fecha



async def consultar_pagos_bd(sesion:Session):

    consulta = (select(
        Pago.id_cuota,
        Pago.fecha,
        Pago.monto,
        Pago.metodo_pago,
        Egresado.nombre.label("nombre_egresado"),
        Cuota.numero_cuota,
        Cuota.estado_pago,
        Curso.id.label("curso_id"),
        Curso.id_escuela,
        Escuela.id,
        Escuela.nombre.label("escuela_nombre")
    ).join(Cuota, Pago.id_cuota == Cuota.id_cuota)
    .join(Egresado, Cuota.id_egresado == Egresado.dni)
    .join(Curso,Egresado.id_curso == Curso.id)
    .join(Escuela,Curso.id_escuela == Escuela.id)
    )
    pagos:Pago = sesion.exec(consulta).all()
    df_pagos = pd.DataFrame([r._asdict() for r in pagos])
    
    return df_pagos



async def generar_pago_bd(sesion:Session,id_cuota:int,monto:Decimal,ruta_comprobante:str):

    metodo_pago = 'Transferecia'
    cobrador = 'admin'
    nuevo_pago:Pago = Pago(id_cuota=id_cuota,monto =monto,metodo_pago=metodo_pago,ruta_comprobante=ruta_comprobante,cobrador=cobrador)

    sesion.add(nuevo_pago)
    sesion.flush()

    return nuevo_pago

def estadisticas_pagos(df_pagos:pd.DataFrame):

    if len(df_pagos)>0:


        df_pagos['fecha'] = pd.to_datetime(df_pagos['fecha'])

        #Obtener pagos realizados
        df_ultimos_pagos = df_pagos[df_pagos['estado_pago'] == 'PAGADO']
        #Ordenar de forma ascendente y tomar los primeros 5
        df_ultimos_pagos = df_ultimos_pagos.sort_values(by='fecha', ascending=True).head(5)
        df_ultimos_pagos['fecha'] = df_ultimos_pagos['fecha'].dt.strftime('%Y-%m-%d')
        estadisticas = {
            'ultimos_pagos': df_ultimos_pagos.to_dict(orient='records')
        }

    else:
        estadisticas = {
            'ultimos_pagos':{}
        }

    return estadisticas