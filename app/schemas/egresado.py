from sqlmodel import Field,Session,SQLModel,select
from models.model_egresado import Egresado


async def obtener_egresados_bd(sesion:Session):
    consulta = select(Egresado)
    resultados = sesion.exec(consulta).all()
    return resultados
    


async def obtener_egresado_dni_bd(sesion:Session,dni:int):
    consulta = select(Egresado).where(Egresado.dni == dni)
    egresado = sesion.exec(consulta).first()
    return egresado


async def agregar_egresado_bd(sesion:Session,nombre:str,dni:int,direccion:str,edad:int,id_escuela:int,id_curso:int,estado_cuenta:str,telefono:str):
    
    egresado = Egresado(nombre=nombre,edad=edad,direccion=direccion,telefono=telefono,id_escuela=id_escuela,id_curso=id_curso,estado_cuenta=estado_cuenta,dni=dni)
    sesion.add(egresado)
    sesion.commit()
    sesion.refresh(egresado)

    return egresado


async def actualizar_egresado_dni_bd(sesion:Session,dni:int,nombre:str,telefono:str,direccion:str):
    consulta = select(Egresado).where(Egresado.dni == dni)
    egresado = sesion.exec(consulta).first()


    egresado.nombre = nombre
    egresado.direccion = direccion
    egresado.telefono = telefono

    sesion.add(egresado)
    sesion.commit()
    sesion.refresh(egresado)

    return egresado

async def eliminar_egresado_bd(sesion:Session,dni:int):
    consulta = select(Egresado).where(Egresado.dni == dni)
    resultados = sesion.exec(consulta)
    egresado = resultados.one()

    sesion.delete(egresado)
    sesion.commit()

    
    return egresado