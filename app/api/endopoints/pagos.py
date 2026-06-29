from fastapi import APIRouter,Request,Depends,Form,status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from models.model_pago import Pago

from schemas.egresado import obtener_egresados_bd,obtener_egresado_dni_bd,agregar_egresado_bd,eliminar_egresado_bd,actualizar_egresado_dni_bd
from api.endopoints.dependencias import obtener_usuario_actual

from core.config import obtener_sesion

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
def cargar_egresado(request:Request,username = Depends(obtener_usuario_actual)):
    
    return templates.TemplateResponse(
        request=request,
        name="egresados/cargar_egresado.html",
        context={
            "username":username
        }
    )


@router.post("/agregar-egresado/")
async def agregar_egresado(request:Request,nombre:str = Form(...),dni:str=Form(...),telefono:str = Form(...),direccion:str = Form(...),edad:str = Form(...),sesion = Depends(obtener_sesion),username = Depends(obtener_usuario_actual)):
    print("Egresado api",nombre)
    await agregar_egresado_bd(sesion,nombre,int(dni),direccion,int(edad),1,2,'AL DIA',telefono)
    
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
    print("Editar")
    egresado = await obtener_egresado_dni_bd(sesion,dni)
    print(egresado)
    return templates.TemplateResponse(
        request=request,
        name = "egresados/egresado.html",
        context={
            "egresado": egresado,
            "username":username
            }
    )



