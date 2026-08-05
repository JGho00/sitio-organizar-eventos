from fastapi import APIRouter,Depends,Request,status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from api.endopoints.dependencias import VerificarRol


from core.config import obtener_sesion

from models.model_escuela import Escuela
from models.model_establecimiento import Establecimiento

from schemas.evento import obtener_eventos_bd,obtener_evento_id_bd
from schemas.establecimiento import obtener_establecimientos_bd
from services.escuela_service import obtener_escuelas_bd

from services import dependencias
from services.evento_service import obtener_eventos_bd_service,estadisticas_eventos,eliminar_evento_bd
router = APIRouter(
    prefix="/eventos",
    tags =["Eventos"],
)

templates = Jinja2Templates("templates")

@router.get("/")
async def get_eventos(request:Request,username = Depends(VerificarRol(['admin'])),sesion = Depends(obtener_sesion)):
    
    if not username:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response
    
    eventos= await obtener_eventos_bd(sesion)
    eventos = eventos.to_dict(orient='records') 
    print("EVENTOS")
    print(eventos)
    escuelas:Escuela = await obtener_escuelas_bd(sesion)

    eventos_service = await obtener_eventos_bd_service(sesion)
    estadisticas = estadisticas_eventos(eventos_service)
    
    estableticimientos:Establecimiento = await obtener_establecimientos_bd(sesion)

    print("eventos",eventos)
    return templates.TemplateResponse(
        request=request,
        name="eventos/eventos.html",
        context={
            "eventos": eventos,
            "username":username,
            "divisiones": dependencias.divisiones,
            "anios": dependencias.anios,
            "interes_mora": dependencias.interes_mora,
            "escuelas": escuelas,
            "establecimientos": estableticimientos,
            'estadisticas':estadisticas
        }
    )

@router.post("/id/{id}")
async def get_evento_id(request:Request,id:int,username = Depends(VerificarRol(['admin'])),sesion = Depends(obtener_sesion)):
    
    if not username:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response

    eventos = await obtener_evento_id_bd(sesion,id)

    return templates.TemplateResponse(
        request=request,
        name="eventos/eventos.html",
        context={
            "egresados": eventos,
            "username":username
        }
    )


@router.post("/eliminar-evento/{id}")
async def eliminar_evento_api(request:Request,id:int,username = Depends(VerificarRol(['admin'])),sesion = Depends(obtener_sesion)):

    try:

        await eliminar_evento_bd(sesion,id)

        sesion.commit()

    except Exception as excepcion_sistema:
        if sesion:
            sesion.rollback()
    finally:
        response = RedirectResponse(url="/eventos", status_code=status.HTTP_303_SEE_OTHER)
        return response