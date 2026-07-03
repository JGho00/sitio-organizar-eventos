from fastapi import APIRouter, Depends, Form, HTTPException,Request,status,UploadFile,File
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from api.endopoints.dependencias import obtener_usuario_actual
import os
from sqlmodel import  Session
from core.config import obtener_sesion


from schemas.contrato import obtener_contratos_bd,obtener_estadisticas_contratos_bd
from schemas.escuela import obtener_escuelas_bd

from services import dependencias
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
    print(type(contratos))
    contratos_estadisticas = await obtener_estadisticas_contratos_bd(sesion)

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

    


