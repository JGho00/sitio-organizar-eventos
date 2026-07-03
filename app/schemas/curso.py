from sqlmodel import Session,select

from models.model_curso import Curso

from core.config import obtener_sesion


async def obtener_cursos_bd(sesion:Session):

    consulta = select(Curso)

    resultado = sesion.exec(consulta)

    cursos = resultado.all()

    return  cursos

async def obtener_curso_bd(sesion:Session, campo: str,valor:any):
    consulta = None
    if 'id' in campo:
        consulta = select(Curso).where(Curso.id ==valor)
    elif 'division' in campo:
        consulta = select(Curso).where(Curso.division == valor)
    
    elif 'año' in campo:
        consulta = select(Curso).where(Curso.año == valor)

    resultado = sesion.exec(consulta)

    curso = resultado.first()

    return  curso


async def crear_curso_bd(sesion:Session,curso:Curso):
    sesion.add(curso)
    sesion.commit()
    sesion.refresh(curso)
    return curso

