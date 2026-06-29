from fastapi import APIRouter, Depends
from fastapi import Request,status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from api.endopoints.dependencias import obtener_usuario_actual
import os
from sqlmodel import Session
from core.config import obtener_sesion

from schemas.contrato import obtener_contratos_bd

templates = Jinja2Templates("templates")

router = APIRouter(
    tags= ["Contratos"],
    prefix="/contratos"
)




templates = Jinja2Templates(directory=os.path.join("templates"))

@router.get("/")
async def consultar_contratos(request: Request,username = Depends(obtener_usuario_actual),sesion: Session = Depends(obtener_sesion)):
    
    if not username:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response
    
    contratos = await obtener_contratos_bd(sesion)
    
    return templates.TemplateResponse(
        request=request,
        name="contratos/contratos.html",
        context={
            
            'username':username,
            'contratos':contratos
        }
    )
