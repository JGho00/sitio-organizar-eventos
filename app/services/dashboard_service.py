from sqlmodel import Session
import pandas as pd
from services.egresado_service import estadisticas_egresado
from services.contrato_service import estadisticas_contratos
from services.cuota_service import consultar_cuotas_bd,estadisticas_cuotas,consultar_cuotas_vencidas
from services.evento_service import estadisticas_eventos
from services.pago_service import consultar_pagos_bd,estadisticas_pagos

async def obtener_estadisticas_generales(sesion:Session):

    resumen_contratos = await estadisticas_contratos(sesion)

    #resumen_egresados = await estadisticas_egresado(sesion)

    resumen_cuotas = await estadisticas_cuotas(sesion)
    print("RESUMEN Cuotas",resumen_cuotas)

    resumen_eventos = await estadisticas_eventos(sesion)

    #5 morosos ordenados por fecha de vencimiento y monto_pago
    df_cuotas:pd.DataFrame = await consultar_cuotas_bd(sesion) 
    df_cuotas_vencidas:pd.Dataframe= consultar_cuotas_vencidas(df_cuotas)
    #df_cuotas_vencidas = df_cuotas_vencidas.head(5)#Test
    dict_cuotas_vencidas:dict = df_cuotas_vencidas.to_dict(orient='records') if not df_cuotas_vencidas.empty else []


    #Ultimos pagos
    df_pagos = await consultar_pagos_bd(sesion)
    resumen_pagos = estadisticas_pagos(df_pagos)
    print(resumen_pagos)
    estadisticas_globales:dict = {

        'contratos': resumen_contratos,
        'cuotas':resumen_cuotas,
        'eventos':resumen_eventos,
        'egresados_morosidad': dict_cuotas_vencidas,
        'pagos':resumen_pagos
    }

    print("Estadisticas")
    print(estadisticas_globales['cuotas'])
    return estadisticas_globales