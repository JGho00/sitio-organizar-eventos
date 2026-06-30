from fastapi import APIRouter, Depends,Request,status,UploadFile,File
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from api.endopoints.dependencias import obtener_usuario_actual
import os
from sqlmodel import Session
from core.config import obtener_sesion

from schemas.contrato import obtener_contratos_bd

from services import contrato_service
templates = Jinja2Templates("templates")

router = APIRouter(
    tags= ["Contratos"],
    prefix="/contratos"
)




templates = Jinja2Templates(directory=os.path.join("templates"))

@router.get("/")
async def consultar_contratos(request: Request,username = Depends(obtener_usuario_actual),sesion: Session = Depends(obtener_sesion)):
    
    if not username:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response
    
    contratos = await obtener_contratos_bd(sesion)
    
    return templates.TemplateResponse(
        request=request,
        name="contratos/contratos.html",
        context={
            
            'username':username,
            'contratos':contratos
        }
    )


@router.post('/carga-masiva-excel')
async def carga_masiva(request:Request,
                       contrato_nombre:str,
                       escuela:str,
                       division:str,
                       monto:str,
                       cantidad_cuotas:str,
                       interes_mora:str,
                       ultimo_dia_pago:str,
                       archivo_egresados:UploadFile = File(...)):


    print(archivo_egresados.filename)

    archivo =await contrato_service.decodificar_archivo_egresados(archivo_egresados)
    df =contrato_service.obtener_df_egresados(archivo)

    print("tabla egresados",df)

    return contrato_nombre,escuela,division,monto,cantidad_cuotas,interes_mora,ultimo_dia_pago