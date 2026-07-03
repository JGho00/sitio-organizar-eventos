from fastapi import APIRouter,Depends,Request,status,UploadFile,File,Form,HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel,Field 
from api.endopoints.dependencias import obtener_usuario_actual


from sqlmodel import Session
from core.config import obtener_sesion

from models.model_evento import Evento
from models.model_escuela import Escuela
from models.model_curso import Curso
from models.model_contrato import Contrato
from models.model_establecimiento import Establecimiento

from schemas.escuela import obtener_escuelas_bd
from schemas.evento import obtener_eventos_bd,obtener_evento_id_bd,obtener_evento_bd,agregar_evento_bd,actualizar_evento_id_bd,eliminar_evento_bd
from schemas.curso import obtener_curso_bd,crear_curso_bd
from schemas.contrato import crear_contrato_bd
from schemas.establecimiento import obtener_establecimientos_bd

from services import dependencias

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
    
    eventos:Evento = await obtener_eventos_bd(sesion)
    print(eventos)
    escuelas:Escuela = await obtener_escuelas_bd(sesion)

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
            "establecimientos": estableticimientos
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
                       monto_total:float = Form(...),
                       interes_mora:float = Form(...),
                       ultimo_dia_pago:str = Form(...),
                       anio:int = Form(...),
                       id_establecimiento:int = Form(...),
                       archivo_egresados:UploadFile = File(...),
                       sesion:Session = Depends(obtener_sesion)):


    #Validar existencia del curso sino crearlo
    curso:Curso = await obtener_curso_bd(sesion, "division", division)
    if not curso:
        curso = Curso(nombre=division,division=division,id_escuela=escuela_id,año=anio)
        curso = await crear_curso_bd(sesion, curso)

    
    
    
    #Crear evento si no existe
    evento = await obtener_evento_bd(sesion,"nombre",evento_nombre)
    if not evento:
        evento = Evento(nombre=evento_nombre,descripcion="",id_curso=curso.id,id_establecimiento=id_establecimiento,estado="creado")
        evento = await agregar_evento_bd(sesion,evento.nombre,evento.descripcion,evento.id_curso,evento.fecha_evento,evento.id_establecimiento,evento.estado)


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


    
    
    print("tabla egresados",df)




    return evento_nombre,escuela_id,division,monto_total,interes_mora,ultimo_dia_pago