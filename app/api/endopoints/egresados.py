from fastapi import APIRouter,Request,Depends,Form
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from schemas.egresado import obtener_egresados_bd,obtener_egresado_dni_bd,agregar_egresado_bd
from api.endopoints.dependencias import obtener_usuario_actual

from core.config import obtener_sesion

router = APIRouter(
    prefix="/egresados",
    tags =["Egresados"],
)


templates = Jinja2Templates( "templates")

@router.get("/")
async def get_egresados(request:Request,username = Depends(obtener_usuario_actual),sesion:Session = Depends(obtener_sesion)):

    egresados = await obtener_egresados_bd(sesion)
    return templates.TemplateResponse(
        request=request,
        name="egresados/egresados.html",
        context={
            "egresados": egresados,
            "username":username
        }
    )


@router.post("/{dni}")
async def get_egresado_dni(request:Request,dni:int):

    egresado = await obtener_egresado_dni_bd(dni)

    return templates.TemplateResponse(
        request=request,
        name = "egresados/egresado.html",
        context={
            "egresado": egresado
        }
    )



@router.get("/agregar-egresado")
def agregar_egresado(request:Request,username = Depends(obtener_usuario_actual)):
    
    return templates.TemplateResponse(
        request=request,
        name="egresados/cargar_egresado.html",
        context={
            "username":username
        }
    )


@router.post("/agregar-egresado/")
async def agregar_egresado(request:Request,nombre:str = Form(...),dni:int=Form(...),telefono:str = Form(...),direccion:str = Form(...),edad:str = Form(...),sesion = Depends(obtener_sesion),username = Depends(obtener_usuario_actual)):
    
    await agregar_egresado_bd(sesion,nombre,dni,direccion,edad,1,2,'AL DIA',telefono)

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
async def get_egresado_dni(request:Request,dni:int,username = Depends(obtener_usuario_actual),sesion:Session = Depends(obtener_sesion)):


    egresados = await obtener_egresados_bd(sesion)
    return templates.TemplateResponse(
        request=request,
        name="egresados/egresados.html",
        context={
            "egresados": egresados,
            "username":username
        }
    )



