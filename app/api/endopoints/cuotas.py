from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from api.endopoints.dependencias import obtener_usuario_actual
import os
from sqlmodel import Session
from core.config import obtener_sesion
from typing import List
import pandas as pd
from models.model_cuota import Cuota
from services.cuota_service import consultar_cuotas_bd,estadisticas_cuotas

templates = Jinja2Templates("templates")

router = APIRouter(
    tags= ["Cuotas"],
    prefix="/cuotas"
)




templates = Jinja2Templates(directory=os.path.join("templates"))

@router.get("/")
async def consultar_cuotas(request: Request,username = Depends(obtener_usuario_actual),sesion_bd: Session = Depends(obtener_sesion)):

    cuotas:pd.Dataframe = await consultar_cuotas_bd(sesion_bd)
    cuotas = cuotas.to_dict(orient='records')
    estadisticas:dict = None
    if cuotas:
        estadisticas = await estadisticas_cuotas(sesion_bd)

    print("CUOTAS")
    print(cuotas)
    return templates.TemplateResponse(
        request=request,
        name="cuotas/cuotas.html",
        context={
            
            'username':username,
            'cuotas': cuotas,
            'estadisticas':estadisticas
        }
    )
