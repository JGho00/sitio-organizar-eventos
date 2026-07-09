from models.model_evento import Evento
from sqlmodel import select,Session
import pandas as pd


from models.model_curso import Curso
from models.model_establecimiento import Establecimiento
from models.model_escuela import Escuela
async def obtener_eventos_bd(sesion:Session):
    consulta = (select(Evento.id,
                      Evento.nombre,
                      Evento.id_curso,
                      Evento.fecha_evento,
                      Evento.id_establecimiento,
                      Curso.id,
                      Curso.id_escuela,
                      Establecimiento.id,
                      Establecimiento.nombre.label("nombre_establecimiento"),
                      Escuela.id,
                      Escuela.nombre.label("nombre_escuela")
                      ).join(Curso, Evento.id_curso == Curso.id)
                      .join(Establecimiento,Evento.id_establecimiento == Establecimiento.id)
                      .join(Escuela,Curso.id_escuela == Escuela.id))
    eventos = sesion.exec(consulta).all()

    #Transformo objeto lista Eventos en Dataframe
    df_eventos = pd.DataFrame([r._asdict() for r in eventos])
    return df_eventos
    


async def obtener_evento_id_bd(sesion:Session,id_evento:int):
    
    consulta = select(Evento).where(Evento.id == id_evento)

    evento = sesion.exec(consulta).first()

    return evento

async def obtener_evento_bd(sesion:Session,campo:str,valor:any):
    
    if 'id' in campo:
        consulta = select(Evento).where(Evento.id == valor)
    elif 'nombre' in campo:
        consulta = select(Evento).where(Evento.nombre == valor)
    
    evento = sesion.exec(consulta).first()

    return evento


async def agregar_evento_bd(sesion:Session,nombre:str,descripcion:str,id_curso:int,fecha_evento:str,id_establecimiento:int,estado:str):
    
    evento = Evento(nombre=nombre,descripcion=descripcion,id_curso=id_curso,fecha_evento=fecha_evento,id_establecimiento=id_establecimiento,estado=estado)
    sesion.add(evento)
    #sesion.commit()
    #sesion.refresh(evento)
    sesion.flush()

    return evento


async def actualizar_evento_id_bd(sesion:Session,id_evento:int,nombre:str,descripcion:str,id_establecimiento:int,fecha:str,estado:str):
    evento:Evento = obtener_evento_id_bd(sesion,id_evento)


    evento.nombre = nombre
    evento.descripcion = descripcion
    evento.id_establecimiento = id_establecimiento
    evento.fecha_evento = fecha
    evento.estado = estado
    

    sesion.add(evento)
    #sesion.commit()
    #sesion.refresh(evento)
    sesion.flush()
    return evento

async def eliminar_evento_bd(sesion:Session,id_evento:int):
    evento = obtener_evento_id_bd(sesion,id_evento)

    sesion.delete(evento)
    #sesion.commit()
    sesion.flush()
    
    return evento

