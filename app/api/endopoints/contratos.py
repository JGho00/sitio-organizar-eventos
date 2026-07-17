from fastapi import APIRouter, Depends,Request,status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from api.endopoints.dependencias import VerificarRol
import os
from sqlmodel import  Session
from core.config import obtener_sesion

from models.model_contrato import Contrato


from services.contrato_service import obtener_contratos_bd,obtener_contrato_id_bd,eliminar_contrato_bd,estadisticas_contratos
from services.escuela_service import obtener_escuelas_bd
from services import dependencias
templates = Jinja2Templates("templates")

router = APIRouter(
    tags= ["Contratos"],
    prefix="/contratos"
)




templates = Jinja2Templates(directory=os.path.join("templates"))

@router.get("/")
async def consultar_contratos(request: Request,username = Depends(VerificarRol(['admin'])),sesion: Session = Depends(obtener_sesion)):
    
    if not username:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response
    
    contratos:Contrato = await obtener_contratos_bd(sesion)
    
    contratos_estadisticas = await estadisticas_contratos(sesion,contratos)

    escuelas = await obtener_escuelas_bd(sesion)
    
    
    return templates.TemplateResponse(
        request=request,
        name="contratos/contratos.html",
        context={
            'anios':dependencias.anios,
            'username':username,
            'contratos':contratos,
            'contratos_estadisticas':contratos_estadisticas,
            'escuelas':escuelas
        }
    )


@router.post("/eliminar-contrato/{id}")
async def consultar_contratos(request: Request,id:int,usuario = Depends(VerificarRol(['admin'])),sesion: Session = Depends(obtener_sesion)):
    
    if not usuario:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response
    
    contrato:Contrato = await obtener_contrato_id_bd(sesion,id)
    print("CONTRATO",contrato)
    contrato = await eliminar_contrato_bd(sesion,contrato)


    sesion.commit()
    return "Contrato eliminado"

    


