from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/favicon.ico", include_in_schema=False)
def get_favicon(name: str):
    return FileResponse("screen.png")