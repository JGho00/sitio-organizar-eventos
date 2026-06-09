from urllib import request

from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


print(os.path.join(BASE_DIR, "templates"))

@router.get("/escuelas",response_class=HTMLResponse)

def listar_escuelas(request: Request):

    
    return templates.TemplateResponse(
        request=request,
        name="escuelas/escuelas.html",
        context={
            "escuelas": escuelas
        }
    )
   
@router.get("/escuelas/{id}")
def obtener_escuela_por_id(id: int, request: Request):
    
    
    for escuela in escuelas:
        if escuela["id"] == id:
            return templates.TemplateResponse(
                request=request,
                name="escuelas/escuela.html",
                context={
                    "escuela": escuela
                }
            )

    return {"error": "Escuela no encontrada"}


@router.post("/escuelas")
def agregar_escuela(escuela: dict,request: Request):
    escuela["id"] = len(escuelas) + 1
    escuelas.append(escuela)
    return templates.TemplateResponse(
        request=request,
        name="escuelas/escuelas.html",
        context={
            "escuelas": escuelas
        }
    )


escuelas = [    
        {
            "id": 1,
            "nombre": "Colegio Nacional",
            "ciudad": "La Rioja",
            "anio": 2026
        },
        {
            "id": 2,
            "nombre": "Escuela Comercial",
            "ciudad": "Chilecito",
            "anio": 2026
        },
        {
            "id": 3,
            "nombre": "Escuela Provincial",
            "ciudad": "La Rioja",
            "anio": 2026
        }
    ]