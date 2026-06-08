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

    escuelas = [
        {
            "nombre": "Colegio Nacional",
            "ciudad": "La Rioja",
            "anio": 2026
        },
        {
            "nombre": "Escuela Comercial",
            "ciudad": "Chilecito",
            "anio": 2026
        }
    ]
    return templates.TemplateResponse(
        request=request,
        name="/escuelas/escuelas.html"
    )
    
    return {"message": "Lista de escuelas", "escuelas": escuelas}
    return {"escuelas": escuelas}

    return templates.TemplateResponse(
        request=request,
        name="/escuelas/escuelas.html",
        context={
            "escuelas": escuelas
        }
    )