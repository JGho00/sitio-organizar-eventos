from models.model_curso import Curso
from sqlmodel import Session,select
from typing import List
import pandas as pd
from schemas.curso import obtener_cursos_bd

async def obtener_cursos_bd_service(sesion:Session):
    consulta = select(Curso)

    resultado = sesion.exec(consulta)

    cursos:List[Curso] = resultado.all()

    df_cursos = pd.DataFrame([r._asdict() for r in cursos])
    return  cursos


async def validar_existencia_curso(sesion:Session,division:str,escuela:int):

    cursos:Curso = await obtener_cursos_bd(sesion)
    
    curso:Curso = None

    for c in cursos:
        if c.division == division and c.id_escuela == escuela:
            curso = c
            break
    return curso