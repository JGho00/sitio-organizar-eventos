from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
import os
router = APIRouter(
    prefix="/egresados",
    tags =["Egresados"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/")
async def get_egresados(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="egresados/egresados.html",
        context={
            "egresados": egresados
        }
    )


egresados = [
    {"id": 1, "nombre": "Juan Pérez", "carrera": "Ingeniería en Sistemas"},
    {"id": 2, "nombre": "María Gómez", "carrera":"Licenciatura en Administración de Empresas"},
    {"id": 3, "nombre": "Carlos Rodríguez", "carrera": "Arquitectura"},
    {"id": 4, "nombre": "Ana Martínez", "carrera": "Medicina"}
]