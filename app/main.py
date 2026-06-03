from fastapi import FastAPI

# Inicializar la aplicación
app = FastAPI()

# Ruta raíz (GET)
@app.get("/")
def leer_raiz():
    return {"mensaje": "¡Hola del mundo real desde FastAPI!"}

# Ruta con parámetros (GET)
@app.get("/items/{item_id}")
def leer_item(item_id: int, q: str = None):
    return {"item_id": item_id, "busqueda": q}