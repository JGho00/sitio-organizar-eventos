from models.model_escuela import Escuela
from sqlmodel import select

import pandas as pd

async def obtener_escuelas_bd(sesion):
    consulta = select(Escuela)
    escuelas = sesion.exec(consulta).all()
    df_escuelas = [e.model_dump() for e in escuelas]
    return df_escuelas

async def obtener_escuela_id(sesion,id):
    consulta = select(Escuela).where(Escuela.id == id)
    escuela = sesion.exec(consulta).first()
    return escuela


async def crear_escuela(sesion_bd,nombre:str,direccion:str,telefono:str):
    
    escuela:Escuela = Escuela(nombre = nombre,direccion = direccion,telefono=telefono)

    sesion_bd.add(escuela)
    sesion_bd.commit()
    sesion_bd.refresh(escuela)

    return escuela

async def editar_escuela_id_bd(sesion_bd,id,campos_valores:dict):
    consulta = select(Escuela).where(Escuela.id == id)
    resultado = sesion_bd.exec(consulta)
    escuela:Escuela = resultado.one()
    
    print(campos_valores)
    for llave, valor in campos_valores.items():
        if llave == 'direccion':
            escuela.direccion = valor
        if llave == 'telefono':
            escuela.telefono = valor


    sesion_bd.add(escuela)
    sesion_bd.commit()
    sesion_bd.refresh(escuela)



async def eliminar_escuela_bd(sesion_bd,id:int):
    consulta = select(Escuela).where(Escuela.id == id)
    resultados = sesion_bd.exec(consulta)
    escuela = resultados.one()

    sesion_bd.delete(escuela)
    sesion_bd.commit()
    
    return escuela


def escuelas_contratos_activas(df_escuelas):
    pass


async def estadisticas_escuela(df_escuelas:pd.DataFrame):
    pass