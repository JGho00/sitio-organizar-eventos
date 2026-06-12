from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
from models.egresado import egresados
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


@router.post("/{dni}")
async def get_egresado_dni(request:Request,dni:int):

    egresado = get_egresado_dni_bd(dni)

    return templates.TemplateResponse(
        request=request,
        name = "egresados/egresado.html",
        context={
            "egresado": egresado
        }
    )



def get_egresado_dni_bd(dni:int):

    egresado_dni:str = ''

    for egresado in egresados:
        if egresado.dni == dni:
            egresado_dni = egresado

    return egresado_dni
