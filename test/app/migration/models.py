from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Создаем базой класс от которого наследуются остальные 
# Нужен для того, чтобы sqlalchemy мог сопоставлять класс с таблицей
Base = declarative_base()


class User(Base):
    """ Класс, который представляет таблицу users """
    __tablename__ = "users"

    # Создаем столбец id, который будет связующим ключом между таблицами
    id = Column(Integer, primary_key=True)
    # Создаем столбец name, содержащий строки длинной до 50 символов
    name = Column(String(50))
    # Создаем столбец age
    age = Column(Integer) 
