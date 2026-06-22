from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from api.endopoints.dependencias import obtener_usuario_actual
import os
from sqlmodel import Session
from core.config import obtener_sesion
templates = Jinja2Templates("templates")

router = APIRouter(
    tags= ["Contratos"],
    prefix="/contratos"
)




templates = Jinja2Templates(directory=os.path.join("templates"))

@router.get("/")
async def consultar_contratos(request: Request,username = Depends(obtener_usuario_actual),sesion_bd: Session = Depends(obtener_sesion)):

    
    return templates.TemplateResponse(
        request=request,
        name="contratos/contratos.html",
        context={
            
            'username':username
        }
    )
