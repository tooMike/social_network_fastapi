from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDbase
from app.models.post import Post
from app.models.users import User
from app.schemas.post import PostCreate


class PostCRUD(CRUDbase):

    async def get_with_author(
            self,
            obj_id: int,
            session: AsyncSession
    ):
        post = await session.execute(
            select(Post, User.username).join(Post.user).where(
                Post.id == obj_id
            )
        )
        post, username = post.first()

        return {
            'id': post.id,
            'author': username,
            'text': post.text,
            'pub_date': post.pub_date,
            'image': post.image,
            'group_id': post.group_id
        }

    async def get_list_with_author(
            self,
            session: AsyncSession
    ):
        posts = await session.execute(
            select(Post, User.username).join(Post.user)
        )
        return [
            {
                'id': post.id,
                'author': username,
                'text': post.text,
                'pub_date': post.pub_date,
                'image': post.image,
                'group_id': post.group_id
            }
            for post, username in posts
        ]


post_crud = PostCRUD(Post)
