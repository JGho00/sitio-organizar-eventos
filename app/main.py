from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.endopoints.egresados import router as egresados_router
from api.endopoints.escuelas import router as escuelas_router
from api.endopoints.eventos import router as eventos_router
from api.endopoints.auth import router as auth_router
from api.endopoints.dashboard import router as dashboard_router
from fastapi.staticfiles import StaticFiles
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Inicializar la aplicación
app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "app", "static")), name="static")
app.include_router(egresados_router)
app.include_router(escuelas_router)
app.include_router(eventos_router)
app.include_router(auth_router)
app.include_router(dashboard_router)

# Ruta de logout global - Redirecciona a /login
@app.get("/logout")
async def logout():
    return RedirectResponse(url="/login", status_code=302)

# Ruta raíz (GET)
@app.get("/")
def leer_raiz():
    return {"mensaje": "¡Hola del mundo real desde FastAPI!"}

# Ruta con parámetros (GET)
@app.get("/items/{item_id}")
def leer_item(item_id: int, q: str = None):
    return {"item_id": item_id, "busqueda": q}