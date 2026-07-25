from fastapi import APIRouter,Request,Depends,status,Form,File,UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse,HTMLResponse,JSONResponse
from sqlmodel import Session

from decimal import Decimal
import pandas as pd
import os
from pathlib import Path
import shutil
from models.model_pago import Pago
from models.model_cuota import Cuota
from models.model_egresado import Egresado
from models.model_escuela import Escuela
from models.model_curso import Curso

from services.pago_service import consultar_pagos_bd,generar_pago_bd,consultar_pago_id_bd
from services.cuota_service import consultar_cuota_id_bd,actualizar_cuota_bd
from api.endopoints.dependencias import VerificarRol

from core.config import obtener_sesion

router = APIRouter(
    prefix="/pagos",
    tags =["Pagos"],
)

carpeta_comprobantes = "media/comprobantes/"
templates = Jinja2Templates( "templates")

@router.get("/")
async def get_pagos(request:Request,username = Depends(VerificarRol(['admin','user'])),sesion:Session = Depends(obtener_sesion)):
    
    
    pagos:pd.DataFrame = await consultar_pagos_bd(sesion)


    
    return pagos.to_dict(orient='records')


@router.get("/{id_cuota}")
async def get_pago_id(request:Request,id_cuota:int,username = Depends(VerificarRol(['admin','user'])),sesion:Session = Depends(obtener_sesion)):
    

    cuota:Cuota = await consultar_cuota_id_bd(sesion,id_cuota)

    pago:Pago = await consultar_pago_id_bd(sesion,id_cuota)

    #Calcular monto por pagar
    monto_por_pagar:float = float(cuota.monto_original) - float(pago.monto)
    

    return templates.TemplateResponse(
            request=request,
            name="pagos/detalle_pago.html",
            context={
                "cuota_id": cuota.id_cuota,
                "monto_cuota":cuota.monto_original,
                "monto_pagado": pago.monto,
                "monto_por_pagar":monto_por_pagar,
                "metodo_pago":pago.metodo_pago,
                "ruta_comprobante":pago.ruta_comprobante
                }
                
        )
    
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
async def registrar_pago_cuota(request:Request,idcuota:int,monto_pagar:Decimal = Form(...),comprobante:UploadFile=File(...),sesion:Session = Depends(obtener_sesion),username = Depends(VerificarRol(['admin','user']))):
    try:

        #Validacion extension del comprobante
        extension:str = os.path.splitext(comprobante.filename)[1].lower()
        if extension not in [".pdf", ".jpg", ".jpeg", ".png"]:
            raise Exception("Comprobante incorrecto")

        
        print("Extension", extension)
        if monto_pagar <= 0:
                raise ValueError("El monto a pagar debe ser mayor a 0.")
        
        
        

        #Validacion si existe la cuota
        print("Id cuota",idcuota)
        cuota:Cuota = await consultar_cuota_id_bd(sesion,idcuota)

        #Capturar egresado al que pertenece la cuota
        egresado:Egresado = cuota.egresado
        print("Egresado", egresado)

        #Capturar curso al que pertenece la cuota a traves del egresado
        curso:Curso = egresado.curso
        print("Curso",curso)

        #Capturar escuela a la pertenece la cuota a traves del egresado y el curso
        escuela:Escuela = curso.escuela
        print("Escuela",escuela)


        #Armar ruta donde se va a almacenar el comprobante enviado
        carpeta_año:str = carpeta_comprobantes+str(curso.año) + '/'
        os.makedirs(carpeta_año,exist_ok=True)
        carpeta_escuela:str= carpeta_año + escuela.nombre + '/'
        os.makedirs(carpeta_escuela,exist_ok=True)
        carpeta_egresado:str = carpeta_escuela + str(egresado.dni)+'_'+egresado.nombre + '/'
        os.makedirs(carpeta_egresado,exist_ok=True)

        
        
        ruta_comprobante:str = carpeta_egresado + comprobante.filename
        objeto_comprobante:Path = Path(ruta_comprobante)

        print("Ruta comprobante",ruta_comprobante)
        try:
            if ruta_comprobante:
                with objeto_comprobante.open("wb") as buffer:
                    shutil.copyfileobj(comprobante.file, buffer)
        except Exception as e:
            print(f"Error al guardar comprobante. Descripción: {str(e)}")
        finally:
            await comprobante.close() 
        print("Cuota existe",idcuota)
        
        
        print("MONNTO",monto_pagar)

        

        pago:Pago = await generar_pago_bd(sesion,cuota.id_cuota,monto_pagar,ruta_comprobante)
        
        cuota_actualizada:Cuota = await actualizar_cuota_bd(sesion,cuota,monto_pagar)

        sesion.commit()


        return JSONResponse(status_code=200, content={"status": "success", "message": "Pago guardado","dni":cuota.id_egresado})
    
    except ValueError as e:
        # Si hay un error controlado de negocio, devolvemos un texto plano con error 400
        return HTMLResponse(status_code=400, content=str(e))
    except Exception as e:
        return HTMLResponse(status_code=500, content="Error interno de servidor.")
