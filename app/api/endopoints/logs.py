from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from api.endopoints.dependencias import VerificarRol
import os
from sqlmodel import Session
from core.config import obtener_sesion
import pandas as pd
from services.log_service import obtener_logs

templates = Jinja2Templates("templates")

router = APIRouter(
    tags= ["Audit Log"],
    prefix="/logs"
)




templates = Jinja2Templates(directory=os.path.join("templates"))

@router.get("/")
async def consultar_cuotas(request: Request,username = Depends(VerificarRol(['admin'])),sesion_bd: Session = Depends(obtener_sesion)):

    logs = await obtener_logs(sesion_bd, username)
    return templates.TemplateResponse(
        request=request,
        name="logs/logs.html",
        context={
            
            'username':username,
            'logs': logs
        }
    )