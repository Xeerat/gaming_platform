from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from os import getenv 
from dotenv import load_dotenv

#=========================================================
# Настройка логирования 
#=========================================================

# Берем текущий config - файл "alembic.ini"
config = context.config
# Проверяем есть ли он
if config.config_file_name is not None:
    # Настраивать логирование в соответствии с параметрами в config
    fileConfig(config.config_file_name)

#=========================================================
# Метаданные моделей (для автогенерации)
#=========================================================

# В данную переменную передаются модели SQLAlchemy 
target_metadata = None

#=========================================================
# Создание URL для связи с базой данных
#=========================================================

load_dotenv()

def get_database_url() -> str:
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
    Функция для генерации SQL-скрипта, без подключения к базе данных.
    """
    # Настройка alembic для работы с базой
    context.configure(
        # Адрес базы 
        url=DB_URL,
        target_metadata=target_metadata,
        # Если параметр включен, то создаем sql запрос с конкретными значениями,
        # который сразу можно применить к базе данных. 
        # Иначе создается sql запрос будет содержать переменные, которые еще необходимо будет потом вставить
        literal_binds=True,
        # Тут обрабатывается, как оформлять переменные в sql запросе
        # В сочетании с literal_binds=True не играет роли
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Создается объект SQLAlchemy Engine 
    # poolclass=pool.NullPool делает так, что никакое соединение не кешировалось,
    # то есть чтобы каждый раз создавалось новое соединение
    connectable = create_engine(DB_URL, poolclass=pool.NullPool)
    # Создается соединение
    with connectable.connect() as connection:
        # Указываем alembic на каком соединении выполнять миграции
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

#=========================================================
# Выбор режима в зависимости от запуска alembic
#=========================================================

# Если был запущен в оффлайн режиме, то оффлайн миграциия
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
