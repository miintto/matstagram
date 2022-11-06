from fastapi.routing import APIRouter

from app.api.auth.route import router as auth_router
from app.api.home.route import router as home_router
from app.api.place.route import router as place_router
from app.api.user.route import router as user_router
from app.client.route import router as client_router

router = APIRouter()


router.include_router(client_router)
router.include_router(home_router)
router.include_router(auth_router, prefix="/api")
router.include_router(place_router, prefix="/api")
router.include_router(user_router, prefix="/api")
