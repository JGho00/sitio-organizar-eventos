from models.model_curso import Curso
from sqlmodel import Session

from schemas.curso import obtener_cursos_bd

async def validar_existencia_curso(sesion:Session,division,escuela):

    cursos:Curso = await obtener_cursos_bd(sesion)
    
    curso:Curso = None

    for c in cursos:
        if c.division == division and c.id_escuela == escuela:
            curso = c
            break
    return curso