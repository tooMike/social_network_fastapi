from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDbase
from app.models.post import Post
from app.models.users import User
from app.schemas.post import PostDB


class PostCRUD(CRUDbase):

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ) -> PostDB:
        post = await session.execute(
            select(Post, User.username).join(Post.user).where(
                Post.id == obj_id))
        post, username = post.first()
        return PostDB(
            id=post.id,
            author=username,
            text=post.text,
            pub_date=post.pub_date,
            image=post.image,
            group_id=post.group_id
        )


    async def get_list(
            self,
            session: AsyncSession
    ):
        # posts = await session.execute(
        #     select(Post, User.username).join(Post.user))
        # return [PostDB(
        #     id=post.id,
        #     author=username,
        #     text=post.text,
        #     pub_date=post.pub_date,
        #     image=post.image,
        #     group_id=post.group_id
        # ) for post, username in posts]
        result = await session.execute(
            select(Post).options(joinedload(Post.user))
        )
        posts = result.scalars().all()
        return [PostDB(
            id=post.id,
            author=post.user.username,
            text=post.text,
            pub_date=post.pub_date,
            image=post.image,
            group_id=post.group_id
        ) for post in posts]



post_crud = PostCRUD(Post)
