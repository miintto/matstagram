from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

router = APIRouter()

template = Jinja2Templates(directory="app/client/templates")


@router.get("/", include_in_schema=False)
def index(request: Request):
    return template.TemplateResponse("index.html", {"request": request})


@router.get("/map", include_in_schema=False)
def index(request: Request):
    return template.TemplateResponse("map.html", {"request": request})
