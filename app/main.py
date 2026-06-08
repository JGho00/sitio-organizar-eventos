from fastapi import FastAPI
from api.endopoints.egresados import router as egresados_router
from api.endopoints.escuelas import router as escuelas_router
from api.endopoints.eventos import router as eventos_router
# Inicializar la aplicación
app = FastAPI()
app.include_router(egresados_router)
app.include_router(escuelas_router)
app.include_router(eventos_router)
# Ruta raíz (GET)
@app.get("/")
def leer_raiz():
    return {"mensaje": "¡Hola del mundo real desde FastAPI!"}

# Ruta con parámetros (GET)
@app.get("/items/{item_id}")
def leer_item(item_id: int, q: str = None):
    return {"item_id": item_id, "busqueda": q}