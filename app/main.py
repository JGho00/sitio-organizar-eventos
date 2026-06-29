from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.endopoints.egresados import router as egresados_router
from api.endopoints.escuelas import router as escuelas_router
from api.endopoints.eventos import router as eventos_router
from api.endopoints.login import router as login_router
from api.endopoints.autenticacion import router as auth_router
from api.endopoints.dashboard import router as dashboard_router
from api.endopoints.contratos import router as contratos_router
from api.endopoints.cuotas import router as cuotas_router
from api.endopoints.usuarios import router as usuarios_router
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel
from core.config import engine
import models as models
from starlette.middleware.sessions import SessionMiddleware
import os
from core.config import SECRET_KEY
SQLModel.metadata.create_all(engine)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Inicializar la aplicación
app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "app", "static")), name="static")
app.include_router(egresados_router)
app.include_router(escuelas_router)
app.include_router(eventos_router)
app.include_router(auth_router)
app.include_router(login_router)
app.include_router(dashboard_router)
app.include_router(contratos_router)
app.include_router(cuotas_router)
app.include_router(usuarios_router)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


# Ruta raíz (GET)
@app.get("/")
def leer_raiz():
    return RedirectResponse(url="/dashboard")

# Ruta con parámetros (GET)
@app.get("/items/{item_id}")
def leer_item(item_id: int, q: str = None):
    return {"item_id": item_id, "busqueda": q}