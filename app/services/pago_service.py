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
from services.dependencias import obtener_fecha



async def consultar_pagos_bd(sesion:Session):

    consulta = (select(
        Pago.id_cuota,
        Pago.fecha,
        Pago.monto,
        Pago.metodo_pago,
        Egresado.nombre.label("nombre_egresado"),
        Cuota.numero_cuota 
    ).join(Cuota, Pago.id_cuota == Cuota.id_cuota)
    .join(Egresado, Cuota.id_egresado == Egresado.dni)
    )
    pagos:Pago = sesion.exec(consulta).all()
    df_pagos = pd.DataFrame([r._asdict() for r in pagos])
    #Convertir los objetos SQLModel a diccionarios
    #cuotas_dict = [cuota.model_dump() for cuota in cuotas]
    
    #Crear y retornar el DataFrame
    #df_cuotas = pd.DataFrame(cuotas_dict)
    
    return df_pagos


def estadisticas_pagos(df_pagos:pd.DataFrame):

    print("ACA PAGOS",df_pagos)

    df_pagos['fecha'] = pd.to_datetime(df_pagos['fecha'])

# 2. Ordenar de forma ascendente y tomar los primeros 5
    df_ultimos_pagos = df_pagos.sort_values(by='fecha', ascending=True).head(5)
    df_ultimos_pagos['fecha'] = df_ultimos_pagos['fecha'].dt.strftime('%Y-%m-%d')
    estadisticas = {
        'ultimos_pagos': df_ultimos_pagos.to_dict(orient='records')
    }

    return estadisticas