from passlib.context import CryptContext
from pydantic import EmailStr
from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi import HTTPException, status

from app.dao.dao_models import UsersDAO
from app.database import get_auth_data

#=========================================================
# Шифрование токена
#=========================================================

# Создаем объект для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict) -> str:
    """ Функция для создания токенов для пользователей """
    to_encode = data.copy()
    # Ставим время действительности токена
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})

    # Получаем особые данные
    auth_data = get_auth_data()
    # Создаем токен для пользователя
    try:
        encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
        return encode_jwt
    except Exception as e:
        raise ValueError(f"Не удалось создать токен: {e}")



#=========================================================
# Шифрование токена
#=========================================================

def decode_access_token(token: str) -> dict:
    """ Функция для расшифровки токена """
    to_decode = token

    auth_data = get_auth_data()
    user_data = jwt.decode(to_decode, auth_data['secret_key'], auth_data['algorithm'])
    return user_data

#=========================================================
# Хеширование пароля
#=========================================================

def get_password_hash(password: str) -> str:
    """ Функция для хеширования паролей пользователей """
    return pwd_context.hash(password)

#=========================================================
# Аутентификация
#=========================================================

async def authenticate_user(email: EmailStr, password: str):
    """ Функция для проверки существования пользователя """
    user = await UsersDAO.find_one_or_none(email=email)
    if not user or pwd_context.verify(password, user.password) is False:
        return None
    return user