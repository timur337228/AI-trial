from fastapi import APIRouter

from backend.api.auth.endpoints import router as auth_router
# from backend.api.ai.endpoints import router as ai_router

router = APIRouter()
router.include_router(router=auth_router)
# router.include_router(router=ai_router)
