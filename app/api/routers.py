from fastapi import APIRouter

from app.api.endpoints import users_router, group_router

main_router = APIRouter()

main_router.include_router(users_router)
main_router.include_router(group_router, prefix="/group", tags=["Group"])


