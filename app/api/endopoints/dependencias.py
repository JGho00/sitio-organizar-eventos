# api/dependencies.py
from fastapi import Request, HTTPException, status
cod_1_token = "ajshdajshdjhasdkjhaskdjhaskjdhakd"
cod_2_token = "32423HJSDJFHSAJHMNASMNDASDasdjhajdjahsdas"

async def obtener_usuario_actual(request: Request) -> str:
    """
    Dependencia global. Revisa la cookie 'access_token'.
    Si no existe o es inválida, redirige al usuario a la página de login.
    """
    token = request.cookies.get("access_token")
    
    if not token:
        # Lanzamos una redirección HTTP 303 hacia la página de login
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/login"}
        )
    
    try:
        # Lógica temporal de limpieza del token ficticio
        token_limpio = token.replace("Bearer ", "")
        username = token_limpio.replace("fake-jwt-token-for-", "")
        username = username.replace(cod_1_token,'').replace(cod_2_token,'').strip()
        print(username)
        
        return username
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/login"}
        )