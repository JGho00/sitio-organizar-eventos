from fastapi import FastAPI,Request,status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse,JSONResponse
from fastapi.exceptions import RequestValidationError
from api.endopoints.egresados import router as egresados_router
from api.endopoints.escuelas import router as escuelas_router
from api.endopoints.eventos import router as eventos_router
from api.endopoints.login import router as login_router
from api.endopoints.autenticacion import router as auth_router
from api.endopoints.dashboard import router as dashboard_router
from api.endopoints.contratos import router as contratos_router
from api.endopoints.cuotas import router as cuotas_router
from api.endopoints.usuarios import router as usuarios_router
from api.endopoints.pagos import router as pagos_router
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel
from core.config import engine
import models as models
from starlette.middleware.sessions import SessionMiddleware
import os
from core.config import SECRET_KEY

from core.logger import logger
SQLModel.metadata.create_all(engine)
import traceback

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Inicializar la aplicación
app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "app", "static")), name="static")
app.mount("/media", StaticFiles(directory=os.path.join(BASE_DIR, "app", "media")), name="media")
app.include_router(egresados_router)
app.include_router(escuelas_router)
app.include_router(eventos_router)
app.include_router(auth_router)
app.include_router(login_router)
app.include_router(dashboard_router)
app.include_router(contratos_router)
app.include_router(cuotas_router)
app.include_router(usuarios_router)
app.include_router(pagos_router)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

templates = Jinja2Templates(directory=os.path.join("templates"))


def es_peticion_ajax(request: Request) -> bool:
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


@app.exception_handler(RequestValidationError)
async def validation_data_exception_handler(request: Request, exc: RequestValidationError):

    errores_legibles = []
    for error in exc.errors():
        campo = error["loc"][-1]
        if error["type"] == "missing":
            mensaje = f"El campo '{campo}' es obligatorio."
        else:
            mensaje = f"El campo '{campo}' tiene un formato inválido."
        errores_legibles.append(mensaje)

    mensaje_general = "El formulario contiene errores de validación."

    if es_peticion_ajax(request):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"mensaje": mensaje_general, "errores": errores_legibles}
        )

    context = {
        "request": request,
        "mensaje": mensaje_general,
        "errores": errores_legibles,
        "url_redireccion": "/eventos"
    }

    return templates.TemplateResponse(
        name="/excepciones/excepcion_422.html",
        context=context,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        request=request
    )



@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    #Define los parámetros que se inyectarán en la plantilla de Jinja2
    error_traceback = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    logger.error(f"Error en la ruta {request.url.path}: {str(exc)}\n{error_traceback}")
    mensaje_general = "Se produjo un error al procesar tu solicitud en el sistema."

    if es_peticion_ajax(request):
        return JSONResponse(status_code=500, content={"mensaje": mensaje_general})

    context = {
        "request": request,
        "mensaje": mensaje_general,
        "url_redireccion": "/dashboard"  # Cambia esto por la ruta de tu app a la que quieras enviar al usuario
    }

    return templates.TemplateResponse(
    name="/excepciones/excepcion_500.html",
    context=context,
    status_code=500,
    request= request
    )
    
# Ruta raíz (GET)
@app.get("/")
def leer_raiz():
    return RedirectResponse(url="/dashboard")

