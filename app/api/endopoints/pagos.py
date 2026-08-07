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

from services.pago_service import consultar_pagos_bd,generar_pago_bd,consultar_pagos_cuota_bd
from services.cuota_service import consultar_cuota_id_bd,actualizar_cuota_bd
from services.log_service import registrar_log_bd
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

    pagos:list[Pago] = await consultar_pagos_cuota_bd(sesion,id_cuota)

    #El monto pagado total se recalcula en base al historial de pagos, no al acumulado cacheado en la cuota
    monto_pagado_total:float = sum(float(pago.monto) for pago in pagos)
    monto_por_pagar:float = float(cuota.monto_original) - monto_pagado_total

    return templates.TemplateResponse(
            request=request,
            name="pagos/detalle_pago.html",
            context={
                "cuota_id": cuota.id_cuota,
                "monto_cuota":cuota.monto_original,
                "monto_pagado": monto_pagado_total,
                "monto_por_pagar":monto_por_pagar,
                "pagos": pagos
                }

        )
    
# 1. Endpoint que arma e inyecta la ventana flotante
@router.get("/cuotas/{cuota_id}/formulario-pago", response_class=HTMLResponse)
async def obtener_formulario_pago(request: Request, cuota_id: int,sesion:Session = Depends(obtener_sesion)):
    
    cuota:Cuota = await consultar_cuota_id_bd(sesion,cuota_id)
    monto_cuota_db = cuota.monto_original

    monto_restante = cuota.monto_original - cuota.monto_pago


    return templates.TemplateResponse(
        request=request,
        name="pagos/formulario_pago.html",
        context={
            "cuota_id": cuota_id,
            "monto_total": monto_cuota_db,
            "restante":monto_restante}
    )


@router.post("/registrar-pago/{idcuota}")
async def registrar_pago_cuota(request:Request,idcuota:int,monto_pagar:Decimal = Form(...),comprobante:UploadFile|None=File(None),sesion:Session = Depends(obtener_sesion),username = Depends(VerificarRol(['admin','user']))):
    try:

        #Validacion extension del comprobante (solo si fue enviado)
        if comprobante and comprobante.filename:
            extension:str = os.path.splitext(comprobante.filename)[1].lower()
            if extension not in [".pdf", ".jpg", ".jpeg", ".png"]:
                raise Exception("Comprobante incorrecto")


        if monto_pagar <= 0:
                raise ValueError("El monto a pagar debe ser mayor a 0.")
        
        
        

        #Validacion si existe la cuota
        cuota:Cuota = await consultar_cuota_id_bd(sesion,idcuota)

        #Capturar egresado al que pertenece la cuota
        egresado:Egresado = cuota.egresado

        #Capturar curso al que pertenece la cuota a traves del egresado
        curso:Curso = egresado.curso

        #Capturar escuela a la pertenece la cuota a traves del egresado y el curso
        escuela:Escuela = curso.escuela


        #Armar ruta donde se va a almacenar el comprobante enviado (solo si fue enviado)
        ruta_comprobante:str|None = None

        if comprobante and comprobante.filename:
            carpeta_año:str = carpeta_comprobantes+str(curso.año) + '/'
            os.makedirs(carpeta_año,exist_ok=True)
            carpeta_escuela:str= carpeta_año + escuela.nombre + '/'
            os.makedirs(carpeta_escuela,exist_ok=True)
            carpeta_egresado:str = carpeta_escuela + str(egresado.dni)+'_'+egresado.nombre + '/'
            os.makedirs(carpeta_egresado,exist_ok=True)

            ruta_comprobante = carpeta_egresado + comprobante.filename
            objeto_comprobante:Path = Path(ruta_comprobante)

            print("Ruta comprobante",ruta_comprobante)
            try:
                with objeto_comprobante.open("wb") as buffer:
                    shutil.copyfileobj(comprobante.file, buffer)
                    print(f"Comprobante almacenado en ruta {ruta_comprobante}")
            except Exception as e:
                print(f"Error al guardar comprobante. Descripción: {str(e)}")
            finally:
                await comprobante.close()
        else:
            print("Sin carga de comprobante")

        print("Cuota existe",idcuota)
        
        
        print("MONNTO",monto_pagar)

        print("COMPROBANTE",ruta_comprobante)

        pago:Pago = await generar_pago_bd(sesion,cuota.id_cuota,monto_pagar,ruta_comprobante)
        
        cuota_actualizada:Cuota = await actualizar_cuota_bd(sesion,cuota,monto_pagar)


        log = await registrar_log_bd(sesion, tipo_accion="REGISTRO PAGO", detalle=f"Se registró un pago de {monto_pagar} para la cuota {cuota.id_cuota} del egresado {egresado.nombre} (DNI: {egresado.dni}).",usuario = username.id_usuario)

        sesion.commit()


        return JSONResponse(status_code=200, content={"status": "success", "message": "Pago guardado","dni":cuota.id_egresado})
    
    except ValueError as e:
        sesion.rollback()
        # Si hay un error controlado de negocio, devolvemos un texto plano con error 400
        return HTMLResponse(status_code=400, content=str(e))
    except Exception as e:
        sesion.rollback()
        return HTMLResponse(status_code=500, content="Error interno de servidor.")
