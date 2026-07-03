from models.model_evento import Evento
from sqlmodel import select,Session



async def obtener_eventos_bd(sesion:Session):
    consulta = select(Evento)
    eventos = sesion.exec(consulta).all()
    return eventos
    


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
    sesion.commit()
    sesion.refresh(evento)

    return evento


async def actualizar_evento_id_bd(sesion:Session,id_evento:int,nombre:str,descripcion:str,id_establecimiento:int,fecha:str,estado:str):
    evento:Evento = obtener_evento_id_bd(sesion,id_evento)


    evento.nombre = nombre
    evento.descripcion = descripcion
    evento.id_establecimiento = id_establecimiento
    evento.fecha_evento = fecha
    evento.estado = estado
    

    sesion.add(evento)
    sesion.commit()
    sesion.refresh(evento)

    return evento

async def eliminar_evento_bd(sesion:Session,id_evento:int):
    evento = obtener_evento_id_bd(sesion,id_evento)

    sesion.delete(evento)
    sesion.commit()

    
    return evento

