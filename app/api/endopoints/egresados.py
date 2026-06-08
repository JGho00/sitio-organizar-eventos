from fastapi import APIRouter

router = APIRouter(
    prefix="/egresados",
    tags =["Egresados"],
)


@router.get("/")
async def get_egresados():
    return {"message": "Lista de egresados"}

