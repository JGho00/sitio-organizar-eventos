from decimal import Decimal,ROUND_CEILING

from fastapi import APIRouter, Depends,Request,status,UploadFile,File,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from api.endopoints.dependencias import VerificarRol,listado_cuotas
import os
from sqlmodel import  Session
from core.config import obtener_sesion

from models.model_contrato import Contrato
from models.model_evento import Evento
from models.model_curso import Curso
from models.model_egresado import Egresado

from services.contrato_service import obtener_contratos_bd,obtener_contrato_id_bd,eliminar_contrato_bd,estadisticas_contratos,crear_contrato_bd
from services.escuela_service import obtener_escuelas_bd
from schemas.establecimiento import obtener_establecimientos_bd
from schemas.evento import obtener_evento_bd,agregar_evento_bd
from schemas.curso import crear_curso_bd
from services.curso_service import validar_existencia_curso
from services.cuota_service import generar_plan_cuotas_egresado
from services import dependencias
templates = Jinja2Templates("templates")

router = APIRouter(
    tags= ["Contratos"],
    prefix="/contratos"
)




templates = Jinja2Templates(directory=os.path.join("templates"))

@router.get("/")
async def consultar_contratos(request: Request,username = Depends(VerificarRol(['admin','user'])),sesion: Session = Depends(obtener_sesion)):
    
    if not username:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response
    
    contratos:Contrato = await obtener_contratos_bd(sesion)
    
    contratos_estadisticas = await estadisticas_contratos(sesion,contratos)

    escuelas = await obtener_escuelas_bd(sesion)

    establecimientos = await obtener_establecimientos_bd(sesion)

    

    return templates.TemplateResponse(
        request=request,
        name="contratos/contratos.html",
        context={
            'anios':dependencias.anios,
            'username':username,
            'contratos':contratos,
            'contratos_estadisticas':contratos_estadisticas,
            'escuelas':escuelas,
            'divisiones':dependencias.divisiones,
            'interes_mora':dependencias.interes_mora,
            'cantidad_cuotas':listado_cuotas,
            'establecimientos':establecimientos
        }
    )


@router.post("/eliminar-contrato/{id}")
async def consultar_contratos(request: Request,id:int,usuario = Depends(VerificarRol(['admin','user'])),sesion: Session = Depends(obtener_sesion)):
    
    if not usuario:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response
    
    contrato:Contrato = await obtener_contrato_id_bd(sesion,id)
    print("CONTRATO",contrato)
    contrato = await eliminar_contrato_bd(sesion,contrato)


    sesion.commit()
    return "Contrato eliminado"


@router.post('/carga-masiva-excel')
async def carga_masiva(
                       evento_nombre:str = Form(...),
                       escuela_id:int = Form(...),
                       division:str = Form(...),
                       monto_total:Decimal = Form(...),
                       interes_mora:float = Form(...),
                       ultimo_dia_pago:str = Form(...),
                       anio:int = Form(...),
                       id_establecimiento:int = Form(...),
                       cantidad_cuotas:str = Form(None),
                       archivo_egresados:UploadFile = File(...),
                       sesion:Session = Depends(obtener_sesion),
                       username = Depends(VerificarRol(['admin','user']))):
                    
    try:

        #Definir cantidad de cuotas.
        cantidad_cuotas = int(cantidad_cuotas) if cantidad_cuotas else 12
        print(f"Cuotas: {cantidad_cuotas}")


        


        #Validar existencia del curso sino crearlo
        curso:Curso = await validar_existencia_curso(sesion,division,escuela_id)
        if not curso:
            print("Curso NO existe:")
            curso = Curso(nombre=division,division=division,id_escuela=escuela_id,año=anio)
            curso = await crear_curso_bd(sesion, curso)


        #Crear evento si no existe
        evento = await obtener_evento_bd(sesion,"nombre",evento_nombre)
        if not evento:
            evento = Evento(nombre=evento_nombre,descripcion="",id_curso=curso.id,id_establecimiento=id_establecimiento,estado="creado")
            evento = await agregar_evento_bd(sesion,evento.nombre,evento.descripcion,evento.id_curso,evento.fecha_evento,evento.id_establecimiento,evento.estado)

        #Formatear monto total para que este redondedo y con dos decimales
        monto_total = monto_total.quantize(Decimal('0.01'),rounding=ROUND_CEILING)

        contrato:Contrato = Contrato(
                                    id_evento=evento.id,
                                    id_curso=curso.id,
                                    fecha_inicio=None,
                                    fecha_fin=None,
                                    monto_total=monto_total,
                                    interes_mora=interes_mora,
                                    dia_vencimiento_mensual=ultimo_dia_pago
                                    )

        nuevo_contrato = await crear_contrato_bd(sesion,contrato)

        #Leer archivo egresados.
        archivo =await dependencias.decodificar_archivo_egresados(archivo_egresados)
        df =dependencias.obtener_df_egresados(archivo)

        egresados:list = []
        for index, row in df.iterrows():
            egresado = {
                "nombre": row["Nombre"],
                "apellido": row["Apellido"],
                "dni": row["Dni"],
                "email": row["Email"],
                "telefono": row["Telefono"],
                "direccion": row["Direccion"],
                "edad": row["Edad"],
                "id_curso":curso.id
            }
            egresados.append(egresado)



        sesion.add_all([Egresado(**egresado) for egresado in egresados])



        #Generar cuotas para cada egresado
        cantidad_egresados: int = len(egresados)
        monto_por_egresado: Decimal = monto_total / cantidad_egresados

        for egresado in egresados:
            await generar_plan_cuotas_egresado(
                id_contrato=nuevo_contrato.id,
                sesion=sesion,
                monto_total_deuda=monto_por_egresado,
                egresado=egresado["dni"],
                dia_vencimiento=int(ultimo_dia_pago),
                cantidad_cuotas=cantidad_cuotas
            )


        #Guardo los cambios
        sesion.commit()




    except Exception as excepcion_sistema:
        print(f'Error en carga masiva: {excepcion_sistema}. Linea: {excepcion_sistema.__traceback__.tb_lineno}')
        if sesion:
            #Por algún error se vuelve atrás la transacción
            sesion.rollback()
        raise excepcion_sistema

    finally:
        response = RedirectResponse(url="/contratos", status_code=status.HTTP_303_SEE_OTHER)
        return response

