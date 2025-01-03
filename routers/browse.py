from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from utils.files import get_html_content

router = APIRouter()

# this has to be the last router to include
@router.get("/{file_path:path}", response_class=HTMLResponse)
def get_html(file_path: str):
    return get_html_content(file_path)