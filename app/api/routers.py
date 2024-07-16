from fastapi import APIRouter

from app.api.endpoints import users_router, group_router, post_router, comment_router

main_router = APIRouter()

main_router.include_router(users_router)
main_router.include_router(group_router, prefix="/group", tags=["Group"])
main_router.include_router(post_router, prefix="/post", tags=["Post"])
main_router.include_router(comment_router, prefix="/post", tags=["Comment"])


