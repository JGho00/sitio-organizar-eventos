from fastapi import APIRouter

router = APIRouter(
    prefix="/eventos",
    tags =["Eventos"],
)

@router.get("/")
async def get_eventos():
    return {"message": "Lista de eventos"}