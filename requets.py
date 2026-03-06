import asyncio
import logging

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from config import db_config
from model import Base, Buttons



class DatabaseManager:
    def __init__(self, dsn):
        self.engine = create_async_engine(dsn, echo=True)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def create_tables(self):
        async with self.async_session() as session:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

    # add new button
    async def add_button(self, button_data):
        async with self.async_session() as session:
            new_button = Buttons(**button_data)
            session.add(new_button)
            await session.commit()
            logging.debug(f'New button added: {new_button}')

    # get button
    async def get_button(self, id_button):
        async with self.async_session() as session:
            result = await session.execute(select(Buttons).where(Buttons.id_button == id_button))
            button = result.scalar()
            logging.debug(f'Get button by id={id_button}')
            return button

    # get all buttons
    async def get_buttons(self):
        async with self.async_session() as session:
            result = await session.execute(select(Buttons))
            buttons = result.scalars().all()
            return buttons

    # update button
    async def update_button(self, button_data: dict, id_button: int = None) -> None:
        async with self.async_session() as session:
            stmt = update(Buttons).where(Buttons.id_button == id_button).values(button_data)
            await session.execute(stmt)
            await session.commit()
            logging.debug(f'Update button by id={id_button}')

    # delete button
    async def delete_button(self, id_button: int) -> None:
        async with self.async_session() as session:
            stmt = delete(Buttons).where(Buttons.id_button == id_button)
            await session.execute(stmt)
            await session.commit()
            logging.debug(f'Delete button by id={id_button}')


async def test(data_button: dict, id_button: int) -> None:
    dsn = db_config()
    db_manager = DatabaseManager(dsn=dsn)
    await db_manager.create_tables()
    await db_manager.add_button(button_data=data_button)
    await db_manager.get_button(id_button=id_button)
    await db_manager.update_button(button_data=data_button, id_button=id_button)
    await db_manager.get_buttons()
    await db_manager.delete_button(id_button=id_button)
    await db_manager.get_button(id_button=id_button)


if __name__ == "__main__":
    asyncio.run(test(data_button={'name':'Test', 'path':'/path'}, id_button=1))