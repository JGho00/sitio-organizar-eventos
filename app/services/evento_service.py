from sqlmodel import Session,select
from sqlalchemy import or_
from typing import List
from models.model_evento import Evento
import pandas as pd
from datetime import datetime
import calendar

from models.model_establecimiento import Establecimiento
from models.model_escuela import Escuela
from models.model_curso import Curso
from models.model_egresado import Egresado
from models.model_contrato import Contrato
from models.model_cuota import Cuota
from models.model_pago import Pago
async def obtener_eventos_bd_service(sesion: Session):
    consulta = (select(Evento.id,
                       Evento.nombre,
                       Evento.fecha_evento,
                       Evento.estado,
                       Establecimiento.id,
                       Establecimiento.nombre.label("nombre_establecimiento"),
                       Curso.id,
                       Curso.id_escuela,
                       Curso.division.label("curso_nombre"),
                       Escuela.id,
                       Escuela.nombre
                       )
                       .join(Establecimiento,Evento.id_establecimiento == Establecimiento.id)
                       .join(Curso,Evento.id_curso == Curso.id)
                       .join(Escuela,Escuela.id == Curso.id_escuela)
                       )
    eventos: List[Evento] = sesion.exec(consulta).all()
    
    df_eventos = pd.DataFrame([r._asdict() for r in eventos])

    if len(df_eventos)>0:
        df_eventos['fecha_evento'] = pd.to_datetime(df_eventos['fecha_evento'])
    
    return df_eventos

async def eliminar_evento_bd(sesion:Session,id_evento:int):
    consulta = select(Evento).where(Evento.id == id_evento)
    resultados = sesion.exec(consulta)
    evento = resultados.first()

    if not evento:
        return evento

    #Egresados del curso asociado al evento
    egresados = sesion.exec(
        select(Egresado).where(Egresado.id_curso == evento.id_curso)
    ).all()
    dnis_egresados = [egresado.dni for egresado in egresados]

    #Contratos generados para este evento
    contratos = sesion.exec(
        select(Contrato).where(Contrato.id_evento == id_evento)
    ).all()
    ids_contratos = [contrato.id for contrato in contratos]

    #Cuotas ligadas a esos egresados o contratos
    cuotas = []
    if dnis_egresados or ids_contratos:
        consulta_cuotas = select(Cuota).where(
            or_(
                Cuota.id_egresado.in_(dnis_egresados),
                Cuota.id_contrato.in_(ids_contratos)
            )
        )
        cuotas = sesion.exec(consulta_cuotas).all()
    ids_cuotas = [cuota.id_cuota for cuota in cuotas]

    #Pagos ligados a esas cuotas
    if ids_cuotas:
        pagos = sesion.exec(
            select(Pago).where(Pago.id_cuota.in_(ids_cuotas))
        ).all()
        for pago in pagos:
            sesion.delete(pago)

    for cuota in cuotas:
        sesion.delete(cuota)

    for egresado in egresados:
        sesion.delete(egresado)

    for contrato in contratos:
        sesion.delete(contrato)

    sesion.delete(evento)
    #sesion.commit()
    sesion.flush()

    return evento

def consultar_eventos_activos(df_eventos):

    condicion = ((df_eventos['estado'] == 'creado'))
    df_eventos_activos:pd.DataFrame = df_eventos[condicion]
    return df_eventos_activos

def consultar_proximo_evento(df_eventos:pd.DataFrame):
    
    #Proximo evento
    fecha_actual = datetime.now()
    proximo_evento:dict = {}
    condicion = (df_eventos["estado"] == "creado") & (
    (df_eventos["fecha_evento"] >= fecha_actual)
    | (df_eventos["fecha_evento"].isna())
    )
    df_proximo_evento:pd.DataFrame = df_eventos[condicion]

    if len(df_proximo_evento) == 0:
        return 
    df_proximo_evento = df_proximo_evento.iloc[0]

    fecha_evento = df_proximo_evento['fecha_evento']
    proximo_evento = {
        'nombre' : df_proximo_evento['nombre'],
        'fecha' : None if pd.isna(fecha_evento) else fecha_evento,
        'lugar' : df_proximo_evento['nombre_establecimiento']
    }

    return proximo_evento


def generar_calendario_eventos(df_eventos:pd.DataFrame):
    
    eventos_activos:pd.DataFrame = consultar_eventos_activos(df_eventos)

    # 3. Obtener mes y año actuales para filtrar y armar la cuadrícula
    hoy = datetime.now()
    anio = hoy.year
    mes = hoy.month

    # 4. Generar la matriz del mes para Jinja2 (Domingo como primer día = 6)
    cal = calendar.Calendar(firstweekday=6)
    semanas_matriz = cal.monthdayscalendar(anio, mes)

    # 5. NUEVO: Filtrar el DataFrame para quedarnos solo con los eventos del mes y año actual
    if not eventos_activos.empty:
        filtro_mes = (eventos_activos['fecha_evento'].dt.year == anio) & \
                     (eventos_activos['fecha_evento'].dt.month == mes) & \
                     (eventos_activos['estado'] == 'creado')
        df_mes_actual = eventos_activos[filtro_mes]
    else:
        df_mes_actual = pd.DataFrame()

    # 6. NUEVO: Agrupar los eventos por el número de día
    # Creamos un diccionario donde la clave es el día (int) y el valor es una lista de diccionarios con los eventos
    eventos_por_dia = {}
    if not df_mes_actual.empty:
        for dia, grupo in df_mes_actual.groupby(df_mes_actual['fecha_evento'].dt.day):
            # Convertimos las filas de este día específico a una lista de diccionarios para Jinja2
            eventos_por_dia[int(dia)] = grupo.to_dict(orient='records')

    # Nombres de meses en español
    meses_es = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    calendario:dict ={
        "semanas": semanas_matriz,
        "eventos_por_dia": eventos_por_dia,
        "mes_nombre": meses_es[mes],
        "anio": anio,
        "dia_actual": hoy.day
    } 

    return calendario

def estadisticas_eventos(df_eventos:pd.DataFrame):

    proximo_evento = None
    df_eventos_finalizados:pd.DataFrame = pd.DataFrame()
    calendario = None
    if len(df_eventos)>0:
        #Proximo evento
        proximo_evento:dict = consultar_proximo_evento(df_eventos)

        #Obtener eventos finalizados (top 5)
        df_eventos_finalizados:pd.DataFrame =df_eventos[df_eventos['estado'] == 'FINALIZADO'].head(5).copy()
        if not df_eventos_finalizados.empty:
            df_eventos_finalizados['fecha_evento'] = df_eventos_finalizados['fecha_evento'].astype(object).where(
                df_eventos_finalizados['fecha_evento'].notna(), None
            )

        #Calendario
        calendario = generar_calendario_eventos(df_eventos)

    estadisticas = {
        'proximo_evento' : proximo_evento,
        'eventos_finalizados':df_eventos_finalizados.to_dict(orient='records'),
        'calendario':calendario
    }
    
        

    
    return estadisticas


