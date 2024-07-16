from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDbase
from app.models.comment import Comment
from app.models.post import Post
from app.models.users import User


class CRUDComment(CRUDbase):
    """Комментарии"""

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

    async def get_with_author(
            self,
            obj_id: int,
            session: AsyncSession
    ):
        comment = await session.execute(
            select(Comment, User.username).join(Comment.user).where(
                Comment.id == obj_id
            )
        )
        comment, username = comment.first()

        return {
            'id': comment.id,
            'author': username,
            'text': comment.text,
            'created': comment.created_at,
            'post': comment.post_id
        }

    async def get_list_with_author(
            self,
            post: Post,
            session: AsyncSession
    ):
        comments = await session.execute(
            select(Comment, User.username).join(Comment.user).filter(
                Comment.post_id == post.id
                )
        )
        return [
            {
                'id': comment.id,
                'author': username,
                'text': comment.text,
                'created': comment.created_at,
                'post': comment.post_id
            }
            for comment, username in comments
        ]


comment_crud = CRUDComment(Comment)
