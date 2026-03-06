from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Buttons(Base):
    __tablename__ = 'buttons'

    id_button: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    path: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        ...
        return f"Button: id: {self.id_button}, name: {self.name}, path: {self.path}"
