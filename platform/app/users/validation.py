from pydantic import BaseModel, EmailStr
from fastapi import Form 

#=========================================================
# Проверка валидности при регистрации
#=========================================================

class SUserRegister(BaseModel):
    """ Класс проверки валидности данных при регистрации """
    email: EmailStr = Form(..., description="Электронная почта")
    password: str = Form(..., min_length=8, max_length=15, description="Пароль, от 8 до 15 знаков")
    username: str = Form(..., min_length=3, max_length=15, description="Username, от 3 до 15 символов")
    confirm_password: str = Form(..., min_length=8, max_length=15, description="Пароль, от 8 до 15 знаков")

#=========================================================
# Проверка валидности при авторизации
#=========================================================

class SUserAuth(BaseModel):
    """ Класс проверки валидности данных при авторизации """
    email: EmailStr = Form(..., description="Электронная почта")
    password: str = Form(..., min_length=8, max_length=15, description="Пароль, от 8 до 15 знаков")