from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDbase
from app.models.comment import Comment
from app.models.post import Post


class CRUDComment(CRUDbase):

    async def get_posts_comment(
            self,
            post: Post,
            comment_id: int,
            session: AsyncSession
    ):
        comment = session.execute(
            select(Comment).where(
                Comment.post_id == post.id,
                Comment.id == comment_id
            )
        )

        return comment


comment_crud = CRUDbase(CRUDComment)
