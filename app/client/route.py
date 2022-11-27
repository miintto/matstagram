from http.cookies import SimpleCookie
import logging

from fastapi import APIRouter, Request
from fastapi.openapi.docs import get_redoc_html
from starlette.templating import Jinja2Templates

from app.common.security.authentication import Authentication

logger = logging.getLogger(__name__)

router = APIRouter()

template = Jinja2Templates(directory="app/client/templates")


@router.get("/", include_in_schema=False)
def index(request: Request):
    return template.TemplateResponse("index.html", {"request": request})


@router.get("/map", include_in_schema=False)
def display_map(request: Request):
    return template.TemplateResponse("map/map.html", {"request": request})


@router.get("/register", include_in_schema=False)
def register(request: Request):
    return template.TemplateResponse(
        "register/register.html", {"request": request}
    )


@router.get("/documents", include_in_schema=False)
async def documents(request: Request):
    cookie = SimpleCookie()
    cookie.load(request.headers.get("Cookie", ""))
    access = cookie.get("access")
    if access:
        try:
            credentials = Authentication.decode_token("cookie", access.value)
            if credentials.payload.permission.is_admin():
                return get_redoc_html(
                    openapi_url="/openapi.json", title="Documents"
                )
        except Exception as e:
            logger.info(f"인증 실패: {e}")
    return template.TemplateResponse(
        "documents/documents.html", {"request": request}
    )
