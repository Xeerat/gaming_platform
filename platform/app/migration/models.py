from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import text
from datetime import datetime

#=========================================================
# Базовый структурная модель
#=========================================================

class Base(AsyncAttrs, DeclarativeBase):
    """ Базовый класс структуры, расширенный до асинхронного """
    # Не создаем для этой модели таблицу
    __abstract__ = True

#=========================================================
# Класс для работы со структорой таблицы users
#=========================================================

class User(Base):
    """ Класс, который представляет структуру таблицы users """
    __tablename__ = "users"

    # Создаем столбцы для таблицы
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_verified: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    register_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    # Говорим, что нужно менять существующую таблицу, а не создавать новую
    extend_existing = True