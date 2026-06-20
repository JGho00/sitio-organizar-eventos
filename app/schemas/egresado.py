from sqlmodel import Field,Session,SQLModel,select
from models.model_egresado import Egresado


async def obtener_egresados_bd(sesion:Session):
    consulta = select(Egresado)
    resultados = sesion.exec(consulta).all()
    return resultados
    


async def obtener_egresado_dni_bd(sesion:Session,dni:int):
    consulta = select(Egresado).where(Egresado.dni == dni)
    egresado = sesion.exec(consulta)
    return egresado


async def agregar_egresado_bd(sesion:Session,nombre:str,dni:int,direccion:str,edad:int,id_escuela:int,id_curso:int,estado_cuenta:str,telefono:str):
    
    egresado = Egresado(nombre=nombre,edad=edad,direccion=direccion,telefono=telefono,id_escuela=id_escuela,id_curso=id_curso,estado_cuenta=estado_cuenta)
    sesion.add(egresado)
    sesion.commit()
    sesion.refresh(egresado)

    return egresado


async def actualizar_egresado_dni_bd(sesion:Session,dni:int,campos_valores:dict):
    consulta = select(Egresado).where(Egresado.dni == dni)
    resultados = sesion.exec(consulta)
    egresado:Egresado = resultados.one()

    print(campos_valores)
    for llave, valor in campos_valores.items():
        if llave == 'direccion':
            Egresado.direccion = valor
        if llave == 'telefono':
            Egresado.telefono = valor

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