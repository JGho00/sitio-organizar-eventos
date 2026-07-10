from fastapi import APIRouter,Request,Depends,Form,status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from schemas.egresado import obtener_egresados_bd,agregar_egresado_bd,eliminar_egresado_bd,actualizar_egresado_dni_bd
from api.endopoints.dependencias import obtener_usuario_actual

from core.config import obtener_sesion

from models.model_curso import Curso

from services.dependencias import divisiones,obtener_fecha
from services.curso_service import validar_existencia_curso
from schemas.escuela import obtener_escuelas_bd
from schemas.curso import crear_curso_bd

from services.egresado_service import obtener_egresado_con_cuotas,estadisticas_egresado

formatos_fechas = obtener_fecha()

router = APIRouter(
    prefix="/egresados",
    tags =["Egresados"],
)


templates = Jinja2Templates( "templates")

@router.get("/")
async def get_egresados(request:Request,username = Depends(obtener_usuario_actual),sesion:Session = Depends(obtener_sesion)):
    
    if not username:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response
    

    egresados = await obtener_egresados_bd(sesion)
    return templates.TemplateResponse(
        request=request,
        name="egresados/egresados.html",
        context={
            "egresados": egresados,
            "username":username
        }
    )

@router.get("/cargar-egresado")
async def cargar_egresado(request:Request,username = Depends(obtener_usuario_actual),sesion:Session = Depends(obtener_sesion)):
    
    escuelas = await obtener_escuelas_bd(sesion)

    return templates.TemplateResponse(
        request=request,
        name="egresados/cargar_egresado.html",
        context={
            "username":username,
            "cursos":divisiones,
            "escuelas": escuelas
        }
    )


@router.post("/agregar-egresado/")
async def agregar_egresado(request:Request,
                           nombre:str = Form(...),
                           dni:str=Form(...),
                           telefono:str = Form(...),
                           direccion:str = Form(...),
                           edad:int = Form(...),
                           division:str = Form(...),
                           escuela_id:int = Form(...),
                           sesion:Session = Depends(obtener_sesion),
                           username = Depends(obtener_usuario_actual)):
    print("ENTRE")
    #Validar existencia del curso sino crearlo
    print("CURSO",division)
    print("ESCUELA",escuela_id)
    curso:Curso = await validar_existencia_curso(sesion,division,escuela_id)
    if not curso:
        print("Curso NO existe:")
        print("CURSO",division)
        curso = Curso(division=division,id_escuela=escuela_id,año=formatos_fechas['yyyy'])
        curso = await crear_curso_bd(sesion, curso)



    await agregar_egresado_bd(sesion,nombre,int(dni),direccion,int(edad),curso.id_escuela,curso.id,telefono)
    sesion.commit()
    egresados = await obtener_egresados_bd(sesion)
    return templates.TemplateResponse(
        request=request,
        name="egresados/egresados.html",
        context={
            "egresados": egresados,
            "username":username
        }
    )





@router.post("/eliminar-egresado/{dni}")
async def eliminar_egresado(request:Request,dni:int,username = Depends(obtener_usuario_actual),sesion:Session = Depends(obtener_sesion)):

    await eliminar_egresado_bd(sesion,dni)

    egresados = await obtener_egresados_bd(sesion)


    return templates.TemplateResponse(
        request=request,
        name="egresados/egresados.html",
        context={
            "egresados": egresados,
            "username":username
        }
    )


@router.post("/actualizar-egresado/{dni}")
async def get_egresado_dni(request:Request,dni:int,nombre:str =Form(...),telefono:str = Form(...),direccion:str = Form(...), username = Depends(obtener_usuario_actual),sesion:Session = Depends(obtener_sesion)):
    print("Dni",dni)
    
    await actualizar_egresado_dni_bd(sesion,dni,nombre,telefono,direccion)

    egresados = await obtener_egresados_bd(sesion)


    return templates.TemplateResponse(
        request=request,
        name="egresados/egresados.html",
        context={
            "egresados": egresados,
            "username":username
        }
    )



@router.post("/dni/{dni}")
async def get_egresado_dni(request:Request,dni:int,sesion:Session = Depends(obtener_sesion),username = Depends(obtener_usuario_actual)):
    
    if not username:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response

    
    egresado = await obtener_egresado_con_cuotas(sesion,dni)

    estadisticas= await estadisticas_egresado(egresado)

    return templates.TemplateResponse(
        request=request,
        name = "egresados/egresado.html",
        context={
            "egresado": egresado,
            "username":username,
            "estadisticas":estadisticas
            }
    )



