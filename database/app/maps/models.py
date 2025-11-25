from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk, created_at
import datetime


class Maps(Base):
    __tablename__ = "maps"
    
    id: Mapped[int_pk]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    created_at: Mapped[created_at]

    name = Column(String(50))
    matrix = Column(ARRAY(Integer, dimensions=2))  # здесь хранится 2D-массив

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"