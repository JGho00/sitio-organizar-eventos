from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi import Request,status
from fastapi.responses import RedirectResponse
from api.endopoints.dependencias import VerificarRol

from sqlmodel import Session
from core.config import obtener_sesion


from services.dashboard_service import obtener_estadisticas_generales
templates = Jinja2Templates("templates")

router = APIRouter(
    tags= ["dashboard"],
    prefix="/dashboard"
)


@router.get("/")
async def cargar_dashboard(request:Request,usuario = Depends(VerificarRol(['admin','user'])),sesion:Session = Depends(obtener_sesion)):
    
    if not usuario:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response
    

    resumen = await obtener_estadisticas_generales(sesion)

    response =  templates.TemplateResponse(
        request=request,
        name="dashboard/dashboard.html",
        context= {
            "request":request,
            "username": usuario,
            'resumen':resumen
                }
            
    )

    print(response.context)

    return response
    


@router.get("/admin-user")
async def cargar_dashboard(request:Request,username = Depends(VerificarRol(['admin']))):
    
    
    print(username)
    
    response =  templates.TemplateResponse(
        request=request,
        name="usuarios/usuarios.html",
        context= {
            "request":request,
            "username": username
                }
    )

    return response