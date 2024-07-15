from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDbase
from app.models.post import Post


class PostCRUD(CRUDbase):

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ):
        post = await session.scalars(
            select(Post, Post.user.username).join(Post.user).where(
                Post.id == obj_id))
        return post.first()


post_crud = PostCRUD(Post)
