from passlib.context import CryptContext
from pydantic import EmailStr
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.dao.dao_models import UsersDAO
from app.database import get_auth_data

from email.mime.text import MIMEText
import smtplib

#=========================================================
# Шифрование токена
#=========================================================

def create_access_token(data: dict) -> str:
    """ Функция для создания токенов для пользователей """
    to_encode = data.copy()
    # Ставим время действительности токена
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})

    # Получаем особые данные
    auth_data = get_auth_data()
    try:
        # Создаем токен для пользователя
        encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
        return encode_jwt
    except Exception as e:
        raise ValueError(f"Не удалось создать токен: {e}")

#=========================================================
# Расшифровка токена
#=========================================================

def decode_access_token(token: str) -> dict:
    """ Функция для расшифровки токена """
    # Получаем особые данные
    auth_data = get_auth_data()
    # Расшифровываем токен
    user_data = jwt.decode(token, auth_data['secret_key'], auth_data['algorithm'])
    return user_data

#=========================================================
# Хеширование пароля
#=========================================================

# Создаем объект для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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


#=========================================================
# Генерация токена для подтверждения email
#=========================================================
def generate_email_token(email: str):
    """Создаёт JWT для подтверждения email"""
    auth_data = get_auth_data()
    payload = {
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }
    return jwt.encode(payload, auth_data["secret_key"], algorithm=auth_data["algorithm"])

#=========================================================
# Отправка письма с подтверждением email
#=========================================================
import smtplib
from email.mime.text import MIMEText
from app.database import get_auth_data  # если используешь эту функцию для секретов

def send_verification_email(to_email, token):
    auth_data = get_auth_data()  # содержит EMAIL_USER и EMAIL_PASSWORD
    verification_link = f"http://localhost:8000/auth/verify-email?token={token}"

    
    
    msg = MIMEText(f"Подтвердите вашу почту: {verification_link}")
    msg["Subject"] = "Подтверждение почты"
    msg["From"] = auth_data["email_user"]         # ваш g.nsu.ru
    msg["To"] = to_email

    with smtplib.SMTP_SSL(auth_data["smtp_server"], auth_data["smtp_port"]) as server:
        server.login(auth_data["email_user"], auth_data["email_password"])
        server.send_message(msg)


#=========================================================
# Пометка email как подтверждённого
#=========================================================

async def mark_user_email_verified(email: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if user:
        await UsersDAO.update({"email": email}, is_verified=True)
        return True
    return False
