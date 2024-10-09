from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models import Post, get_async_session
#from typing import AsyncGenerator


async def get_last_announcement_info() -> str:
    async with get_async_session() as session:
        result = await session.execute(select(Post))
        post = result.scalars().one()  # Получаем пост
        return post


async def is_posts_the_same():
    ...


async def add_post(header: str, content: str):
    async with get_async_session() as session:  # Асинхронное открытие сессии
        async with session.begin():  # Начало транзакции
            new_post = Post(header=header, content=content)  # Создаем новый объект
            session.add(new_post)  # Добавляем объект в сессию (await не нужен для add)
        await session.commit()  # Сохраняем изменения в базе данных

