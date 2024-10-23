from sqlalchemy import select

from datadase.models import Post, get_async_session


async def get_last_announcement_from_db() -> str:
    async with get_async_session() as session:
        result = await session.execute(select(Post))
        post = result.scalars().one()
        return post.header


async def are_posts_the_same(post_from_db, post_from_website) -> bool:
    return post_from_db == post_from_website


async def add_post(header: str, content: str):
    async with get_async_session() as session:  # Асинхронное открытие сессии
        async with session.begin():  # Начало транзакции
            new_post = Post(header=header, content=content)  # Создаем новый объект
            session.add(new_post)  # Добавляем объект в сессию (await не нужен для add)
        await session.commit()  # Сохраняем изменения в базе данных


async def update_post(header, content):
    async with get_async_session() as session:
        async with session.begin():
            post = await session.get(Post, 1)

            if post:
                post.header = header
                post.content = content

            else:
                post = Post(id=1, header=header, content=content)
                session.add(post)

        await session.commit()
