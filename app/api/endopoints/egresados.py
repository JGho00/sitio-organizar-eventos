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


