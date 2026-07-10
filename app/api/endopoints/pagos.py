from fastapi import APIRouter,Request,Depends,status,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse,HTMLResponse,JSONResponse
from sqlmodel import Session

from decimal import Decimal
import pandas as pd

from models.model_pago import Pago
from models.model_cuota import Cuota
from services.pago_service import consultar_pagos_bd,generar_pago_bd
from services.cuota_service import consultar_cuota_id_bd,actualizar_cuota_bd
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


# 1. Endpoint que arma e inyecta la ventana flotante
@router.get("/cuotas/{cuota_id}/formulario-pago", response_class=HTMLResponse)
async def obtener_formulario_pago(request: Request, cuota_id: int,sesion:Session = Depends(obtener_sesion)):
    
    cuota:Cuota = await consultar_cuota_id_bd(sesion,cuota_id)
    monto_cuota_db = cuota.monto_original
    


    return templates.TemplateResponse(
        request=request,
        name="pagos/formulario_pago.html",
        context={"cuota_id": cuota_id, "monto_total": monto_cuota_db}
    )


@router.post("/registrar-pago/{idcuota}")
async def registrar_pago_cuota(request:Request,idcuota:int,username = Depends(obtener_usuario_actual),monto_pagar:Decimal = Form(...),sesion:Session = Depends(obtener_sesion)):
    try:
        if not username:
            response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
            response.delete_cookie("access_token")
            return response
        

        if monto_pagar <= 0:
                raise ValueError("El monto a pagar debe ser mayor a 0.")
        
        print("Id cuota",idcuota)


        #Validacion si existe la cuota
        cuota:Cuota = await consultar_cuota_id_bd(sesion,idcuota)

        
        print("Cuota existe",idcuota)
        
        
        print("MONNTO",monto_pagar)

        

        pago:Pago = await generar_pago_bd(sesion,cuota.id_cuota,monto_pagar)
        
        cuota_actualizada = await actualizar_cuota_bd(sesion,cuota,monto_pagar)

        sesion.commit()


        return JSONResponse(status_code=200, content={"status": "success", "message": "Pago guardado","dni":cuota.id_egresado})
    
    except ValueError as e:
        # Si hay un error controlado de negocio, devolvemos un texto plano con error 400
        return HTMLResponse(status_code=400, content=str(e))
    except Exception as e:
        return HTMLResponse(status_code=500, content="Error interno de servidor.")
