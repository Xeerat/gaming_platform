## Так обозначаются комментариии для mako-файла, поэтому 

## Теперь к коду, это просто python код, который будет переносится в файлы миграции.
## Ниже находится описание миграции: сообщение при создании, id, предыдущая миграция и т.д
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

## Если alembic при автогенерации посчитает, что ему нужны еще импорты, то он их добавит с помощью этой строки 
${imports if imports else ""}

## Переменные для связи миграций для alembic
revision: str = ${repr(up_revision)}
down_revision: Union[str, Sequence[str], None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}

## Функция для обновления таблицы у отдельного пользователя 
def upgrade() -> None:
    """Upgrade schema."""
    ## Если есть обновления, то alembic применяет их самостоятельно 
    ${upgrades if upgrades else "pass"}

## Функция для отката миграции у отдельного пользователя 
def downgrade() -> None:
    """Downgrade schema."""
    ## Если нужно сделать откат, то alembic сделает его самостоятельно 
    ${downgrades if downgrades else "pass"}
