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
from api.endopoints.logs import router as logs_router
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
app.include_router(logs_router)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

templates = Jinja2Templates(directory=os.path.join("templates"))


def es_peticion_ajax(request: Request) -> bool:
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


# Mensajes legibles por campo, agrupados por ruta del formulario que los origina.
MENSAJES_CAMPO_POR_RUTA = {
    "/contratos/carga-masiva-excel": {
        "evento_nombre": {"faltante": "No se agregó el nombre del evento.", "invalido": "El nombre del evento no es válido."},
        "escuela_id": {"faltante": "No se agregó la escuela.", "invalido": "La escuela seleccionada no es válida."},
        "division": {"faltante": "No se agregó la división.", "invalido": "La división no es válida."},
        "monto_total": {"faltante": "No se agregó el monto total.", "invalido": "El monto total ingresado no es válido."},
        "interes_mora": {"faltante": "No se agregó el interés por mora.", "invalido": "El interés por mora ingresado no es válido."},
        "ultimo_dia_pago": {"faltante": "No se definió el último día de la fecha de pago.", "invalido": "El último día de la fecha de pago no es válido."},
        "anio": {"faltante": "No se agregó el año del contrato.", "invalido": "El año del contrato no es válido."},
        "id_establecimiento": {"faltante": "No se agregó el establecimiento.", "invalido": "El establecimiento seleccionado no es válido."},
        "archivo_egresados": {"faltante": "No se adjuntó el archivo de egresados.", "invalido": "El archivo de egresados no es válido."},
    },
}

# Título de la ventana emergente de error, según la ruta del formulario que la origina.
TITULOS_ERROR_POR_RUTA = {
    "/contratos/carga-masiva-excel": "Error al generar contrato",
}


@app.exception_handler(RequestValidationError)
async def validation_data_exception_handler(request: Request, exc: RequestValidationError):

    ruta = request.url.path
    mensajes_campo = MENSAJES_CAMPO_POR_RUTA.get(ruta, {})
    titulo = TITULOS_ERROR_POR_RUTA.get(ruta, "Errores de validación")

    errores_legibles = []
    for error in exc.errors():
        campo = str(error["loc"][-1])
        mensajes_de_este_campo = mensajes_campo.get(campo)
        if error["type"] == "missing":
            mensaje = mensajes_de_este_campo["faltante"] if mensajes_de_este_campo else f"El campo '{campo}' es obligatorio."
        else:
            mensaje = mensajes_de_este_campo["invalido"] if mensajes_de_este_campo else f"El campo '{campo}' tiene un formato inválido."
        errores_legibles.append(mensaje)

    mensaje_general = errores_legibles[0] if len(errores_legibles) == 1 else "El formulario contiene errores de validación."

    if es_peticion_ajax(request):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"titulo": titulo, "mensaje": mensaje_general, "errores": errores_legibles}
        )

    context = {
        "request": request,
        "titulo": titulo,
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

