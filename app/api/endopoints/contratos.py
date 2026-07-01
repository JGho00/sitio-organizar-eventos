from fastapi import APIRouter, Depends,Request,status,UploadFile,File
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from api.endopoints.dependencias import obtener_usuario_actual
import os
from sqlmodel import Session
from core.config import obtener_sesion

from schemas.contrato import obtener_contratos_bd
from schemas.escuela import obtener_escuelas_bd

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

    escuelas = await obtener_escuelas_bd(sesion)
    
    
    return templates.TemplateResponse(
        request=request,
        name="contratos/contratos.html",
        context={
            'anios':contrato_service.anios,
            'username':username,
            'contratos':contratos,
            'escuelas':escuelas,
            'divisiones':contrato_service.divisiones,
            'interes_mora':contrato_service.interes_mora
        }
    )


@router.post('/carga-masiva-excel')
async def carga_masiva(request:Request,
                       contrato_nombre:str,
                       escuela:str,
                       division:str,
                       monto:float,
                       cantidad_cuotas:int,
                       interes_mora:float,
                       ultimo_dia_pago:str,
                       archivo_egresados:UploadFile = File(...),
                       sesion:Session = Depends(obtener_sesion)):


    ##Validar escuela
    escuelas = await obtener_escuelas_bd(sesion=sesion)
    for escuela_bd in escuelas:
        if escuela_bd.nombre == escuela:
            break
    else:
        return {"error": "La escuela no existe en la base de datos"}

    archivo =await contrato_service.decodificar_archivo_egresados(archivo_egresados)
    df =contrato_service.obtener_df_egresados(archivo)

    print("tabla egresados",df)

    return contrato_nombre,escuela,division,monto,cantidad_cuotas,interes_mora,ultimo_dia_pago