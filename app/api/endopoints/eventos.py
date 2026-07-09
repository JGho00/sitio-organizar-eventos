from decimal import Decimal,ROUND_CEILING

from fastapi import APIRouter,Depends,Request,status,UploadFile,File,Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from api.endopoints.dependencias import obtener_usuario_actual


from sqlmodel import Session
from core.config import obtener_sesion

from models.model_evento import Evento
from models.model_escuela import Escuela
from models.model_curso import Curso
from models.model_contrato import Contrato
from models.model_egresado import Egresado
from models.model_establecimiento import Establecimiento

from schemas.escuela import obtener_escuelas_bd
from schemas.evento import obtener_eventos_bd,obtener_evento_id_bd,obtener_evento_bd,agregar_evento_bd
from schemas.curso import crear_curso_bd
from services.contrato_service import crear_contrato_bd
from schemas.establecimiento import obtener_establecimientos_bd

from services import dependencias
from services.curso_service import validar_existencia_curso
from services.cuota_service import generar_plan_cuotas_egresado
from services.evento_service import obtener_eventos_bd_service,estadisticas_eventos
router = APIRouter(
    prefix="/eventos",
    tags =["Eventos"],
)

templates = Jinja2Templates("templates")

@router.get("/")
async def get_eventos(request:Request,username = Depends(obtener_usuario_actual),sesion = Depends(obtener_sesion)):
    
    if not username:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response
    
    eventos= await obtener_eventos_bd(sesion)
    eventos = eventos.to_dict(orient='records') 
    print("EVENTOS")
    print(eventos)
    escuelas:Escuela = await obtener_escuelas_bd(sesion)

    eventos_service = await obtener_eventos_bd_service(sesion)
    estadisticas = estadisticas_eventos(eventos_service)
    
    estableticimientos:Establecimiento = await obtener_establecimientos_bd(sesion)

    print("eventos",eventos)
    return templates.TemplateResponse(
        request=request,
        name="eventos/eventos.html",
        context={
            "eventos": eventos,
            "username":username,
            "divisiones": dependencias.divisiones,
            "anios": dependencias.anios,
            "interes_mora": dependencias.interes_mora,
            "escuelas": escuelas,
            "establecimientos": estableticimientos,
            'estadisticas':estadisticas
        }
    )

@router.post("/id/{id}")
async def get_evento_id(request:Request,id:int,username = Depends(obtener_usuario_actual),sesion = Depends(obtener_sesion)):
    
    if not username:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response

    eventos = await obtener_evento_id_bd(sesion,id)

    return templates.TemplateResponse(
        request=request,
        name="eventos/eventos.html",
        context={
            "egresados": eventos,
            "username":username
        }
    )


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
                       archivo_egresados:UploadFile = File(...),
                       sesion:Session = Depends(obtener_sesion)):

    try:
    


        print("Id escuela:",escuela_id)


        #Validar existencia del curso sino crearlo
        curso:Curso = await validar_existencia_curso(sesion,division,escuela_id)
        if not curso:
            print("Curso NO existe:")
            curso = Curso(nombre=division,division=division,id_escuela=escuela_id,año=anio)
            curso = await crear_curso_bd(sesion, curso)

        else:
            print("Curso existe:")
        
        
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
                cantidad_cuotas=12
            )


        #Guardo los cambios
        sesion.commit()

        
        
    
    except Exception as excepcion_sistema:
        print(f'Error en carga masiva: {excepcion_sistema}. Linea: {excepcion_sistema.__traceback__.tb_lineno}')
        if sesion:
            #Por algún error se vuelve atrás la transacción
            sesion.rollback()

    finally:
        response = RedirectResponse(url="/eventos", status_code=status.HTTP_303_SEE_OTHER)
        return response