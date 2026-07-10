from fastapi import APIRouter,Request,Depends,status,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Session
import pandas as pd

from models.model_pago import Pago
from models.model_cuota import Cuota
from services.pago_service import consultar_pagos_bd
from services.cuota_service import consultar_cuotas_bd,consultar_cuota_id_bd
from api.endopoints.dependencias import obtener_usuario_actual

from core.config import obtener_sesion

router = APIRouter(
    prefix="/pagos",
    tags =["pagos"],
)


templates = Jinja2Templates( "templates")

@router.get("/")
async def get_pagos(request:Request,username = Depends(obtener_usuario_actual),sesion:Session = Depends(obtener_sesion)):
    
    if not username:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response
    

    pagos:pd.DataFrame = await consultar_pagos_bd(sesion)


    
    return pagos.to_dict(orient='records')



@router.post("/registrar-pago/{id_cuota}")
async def registrar_pago_cuota(request:Request,id_cuota:int,username = Depends(obtener_usuario_actual),sesion:Session = Depends(obtener_sesion)):
    
    if not username:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response
    
    print("Numero_cuota",id_cuota)


    #Validacion si existe la cuota
    cuota:Cuota = await consultar_cuota_id_bd(sesion,id_cuota)
    
    if not cuota:
        return "No existe la cuota"
    
    print("Cuota existe",id_cuota)
    
    
    


    
