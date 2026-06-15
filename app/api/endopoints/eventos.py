from fastapi import APIRouter,Response,Depends,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from api.endopoints.dependencias import obtener_usuario_actual
from models.evento import eventos


router = APIRouter(
    prefix="/eventos",
    tags =["Eventos"],
)

templates = Jinja2Templates("templates")

@router.get("/")
async def get_eventos(request:Request,username = Depends(obtener_usuario_actual)):
    #response = templates.TemplateResponse(name="/eventos/")
    return eventos 