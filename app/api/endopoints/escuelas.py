from models.escuela import escuelas
from fastapi import APIRouter,Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from api.endopoints.dependencias import obtener_usuario_actual
import os

router = APIRouter(
    prefix="/escuelas",
    tags=["escuelas"]
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


print(os.path.join(BASE_DIR, "templates"))

@router.get("/",response_class=HTMLResponse)
def listar_escuelas(request: Request,username = Depends(obtener_usuario_actual)):

    
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
        if escuela.id == id:
            return templates.TemplateResponse(
                request=request,
                name="escuelas/escuela.html",
                context={
                    "escuela": escuela
                }
            )

    return {"error": "Escuela no encontrada"}


@router.post("/escuelas/{id}")
def agregar_escuela(escuela: dict,request: Request):
    try:
        escuela["id"] = len(escuelas) + 1
    except Exception as e:
        return {"error": str(e)}
    escuelas.append(escuela)
    return templates.TemplateResponse(
        request=request,
        name="escuelas/escuelas.html",
        context={
            "escuelas": escuelas
        }
    )

@router.delete("/escuelas/{id}")
def eliminar_escuela(id: int,request: Request):
    print(id)
    for escuela in escuelas:
        if escuela["id"] == id:
            escuelas.remove(escuela)
            return templates.TemplateResponse(
                request=request,
                name="escuelas/escuelas.html",
                context={
                    "escuelas": escuelas
                }
            )
    return {"error": "Escuela no encontrada"}


