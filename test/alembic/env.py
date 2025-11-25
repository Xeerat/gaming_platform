from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from os import getenv 
from dotenv import load_dotenv
from app.migration.models import Base

#=========================================================
# Настройка логирования 
#=========================================================

# Берем текущий config - файл "alembic.ini"
config = context.config
# Проверяем есть ли он
if config.config_file_name is not None:
    # Настраиваем логирование в соответствии с параметрами в config
    fileConfig(config.config_file_name)

#=========================================================
# Метаданные моделей (для автогенерации)
#=========================================================

# В данную переменную передаются модели SQLAlchemy 
target_metadata = Base.metadata

#=========================================================
# Создание URL для связи с базой данных
#=========================================================

# Загружаем переменные среды из файла .env
load_dotenv()

def get_database_url() -> str:
    """ Функция, которая формирует URL для взаимодействия с базой данных. """
    user = getenv("DB_USER")
    password = getenv("DB_PASSWORD")
    host = getenv("DB_HOST")
    port = getenv("DB_PORT")
    name = getenv("DB_NAME")
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"

DB_URL = get_database_url()

#=========================================================
# Оффлайн режим
#=========================================================

def run_migrations_offline() -> None:
    """ 
    Функция для генерации SQL-скрипта без дальнейшего выполнения.
    Подключение к базе данных не происходит.
    """
    # Настройка alembic для работы с базой
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        # Вставлять ли конкретные значения в sql-запрос или добавлять переменные?
        literal_binds=True,
        # Вид переменных в sql-запросе. В сочетании с literal_binds=True не играет роли
        dialect_opts={"paramstyle": "named"},
    )

    # Создается контекст транзакции для миграции. Это как бы оболочка для миграции
    # Это значит, что все изменения, которые будут применяться, оборачиваются в эту транзакцию
    # Если что-то пойдет не так, то транзакция откатится и база данных не пострадает
    # После этого блока изменения либо применяются, либо откатываются с ошибкой
    with context.begin_transaction():
        # Функция выполняет все миграции, которые не применены 
        context.run_migrations()


#=========================================================
# Онлайн режим
#=========================================================

def run_migrations_online() -> None:
    """ 
    Функция для генерации и дальнейшего выполнения SQL-скрипта.
    Происходит подключение к базе данных.
    """
    # Создается объект SQLAlchemy Engine 
    # poolclass=pool.NullPool делает так, чтобы каждый раз создавалось новое соединение, а старое не сохранялось
    connectable = create_engine(DB_URL, poolclass=pool.NullPool)
    # Создается соединение
    with connectable.connect() as connection:
        # Настраиваем alembic для работы с базой
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

#=========================================================
# Выбор режима в зависимости от запуска alembic
#=========================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
