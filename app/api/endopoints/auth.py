from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import RedirectResponse
from models.usuario import usuarios_db

templates = Jinja2Templates("templates")
token:str = "ajshdajshdjhasdkjhaskdjhaskjdhakdUSER32423HJSDJFHSAJHMNASMNDASDasdjhajdjahsdas"

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
    
    token_access = token.replace('USER',form_data.username)
    print(token_access)
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    response.set_cookie(
        key="access_token", 
        value=f"Bearer {token_access}", # El estándar OAuth2 requiere la palabra Bearer
        httponly=True,                    # Protege contra robos por JavaScript
        max_age=1800,                     # Tiempo de vida: 30 minutos (en segundos)
        secure=False,                     # Cambia a True en producción (solo HTTPS)
        samesite="lax" 
    )
    
    return response
    


@router.get("/logout")
async def logout_from_login(request: Request):
    # Redirige a la ruta /logout global
    response =  RedirectResponse(url="/logout", status_code=302)
    response.delete_cookie("access_token")

    return response