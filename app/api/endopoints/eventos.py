from fastapi import APIRouter,Depends,Request
from fastapi.templating import Jinja2Templates
from api.endopoints.dependencias import obtener_usuario_actual
from models.evento import eventos

#IMPORT MODELOS
from sqlmodel import Session
from core.config import obtener_sesion
from models.model_evento import Evento
from schemas.evento import obtener_eventos_bd,obtener_evento_id_bd,agregar_evento_bd,actualizar_evento_id_bd,eliminar_evento_bd

router = APIRouter(
    prefix="/eventos",
    tags =["Eventos"],
)

templates = Jinja2Templates("templates")

@router.get("/")
async def get_eventos(request:Request,username = Depends(obtener_usuario_actual),sesion = Depends(obtener_sesion)):
    
    eventos = await obtener_eventos_bd(sesion)
    print(eventos)
    return templates.TemplateResponse(
        request=request,
        name="eventos/eventos.html",
        context={
            "eventos": eventos,
            "username":username
        }
    )

@router.post("/id/{id}")
async def get_evento_id(request:Request,id:int,username = Depends(obtener_usuario_actual),sesion = Depends(obtener_sesion)):
    
    eventos = await obtener_evento_id_bd(sesion,id)

    return templates.TemplateResponse(
        request=request,
        name="eventos/eventos.html",
        context={
            "egresados": eventos,
            "username":username
        }
    )