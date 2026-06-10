from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter(
    prefix="/login",
    tags =["Login"],
)

#Obtengo la ruta del proyecto "app"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/")
async def login(request:Request):
    
    return templates.TemplateResponse(
        request=request,
        name="login/login.html",
        context={
            "request": request
        }
    )

@router.post("/")
async def login_post(username: str, password: str, request: Request):
    print("Recibiendo datos de login...")
    print(request)
    form_data = await request.form()
    username = form_data.get("usuario")
    password = form_data.get("password")
    
    # Aquí puedes agregar la lógica de autenticación, por ejemplo, verificar el usuario y contraseña en una base de datos.
    
    if username == "admin" and password == "admin":
        return {"message": "Inicio de sesión exitoso"}
    else:
        return {"message": "Credenciales inválidas"}
    

