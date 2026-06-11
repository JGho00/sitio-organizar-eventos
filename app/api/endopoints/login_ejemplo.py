from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import RedirectResponse
from models.usuario import usuarios_db

templates = Jinja2Templates("templates")

router = APIRouter(
    prefix="/login",
    tags=["Login"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

@router.get("/")
async def login(request:Request):
    
    return templates.TemplateResponse(
        request=request,
        name="login/login.html",
        context={
            "request": request
        }
    )


@router.post("/token")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    
    print(f"Username: {form_data.username}, Password: {form_data.password}")
    
    if form_data.username not in usuarios_db:
        print("Usuario no encontrado")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if form_data.password != usuarios_db[form_data.username]["hashed_password"]:
        print("Credenciales incorrectas")
        print(form_data.password,usuarios_db[form_data.username]["hashed_password"])
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return templates.TemplateResponse(
        request=request,
        name="dashboard/dashboard.html",
        context={
            "username": form_data.username
        }
    )


@router.get("/logout")
async def logout_from_login(request: Request):
    # Redirige a la ruta /logout global
    return RedirectResponse(url="/logout", status_code=302)
