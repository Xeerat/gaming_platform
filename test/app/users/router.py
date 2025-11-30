from fastapi import APIRouter, HTTPException, status, Response, Form, Request
from fastapi.responses import RedirectResponse
from pydantic import EmailStr

from app.dao.dao_models import UsersDAO
from app.users.validation import SUserRegister, SUserAuth
import app.users.auth as auth


# Создаем объект, который будет содержать все маршруты
# Они все будут начинаться с /auth
router = APIRouter(prefix='/auth', tags=['Auth'])

#=========================================================
# Маршрут /auth/registrer/
#=========================================================

# post обозначает, что функция создает и изменяет данные на сервере
@router.post("/register/")
async def register_user(
    response: Response, 
    email: EmailStr = Form(...),
    password: str = Form(...),
    username: str = Form(...),
    confirm_password: str = Form(...)
) -> dict:
    """ Функция для регистрации пользователя """
    user_data = SUserRegister(
        email=email,
        password=password,
        username=username,
        confirm_password=confirm_password
    )
    # Ищем пользователя по email
    found_user = await UsersDAO.find_one_or_none(email=user_data.email)
    # Если пользователь уже существует, то ошибка
    if found_user:
        return RedirectResponse(
            "/auth/register/?error=Пользователь+с+таким+email+уже+существует.",
            status_code=303
            )
    
    # Ищем пользователя по никнейму
    found_user = await UsersDAO.find_one_or_none(username=user_data.username)
    if found_user:
        return RedirectResponse(
            "/auth/register/?error=Пользователь+с+таким+именем+уже+существует!",
            status_code=303
        )
    
    # Превращаем объект SUserRegister в словарь
    user_dict = user_data.dict()
    
    del user_dict["confirm_password"]
    if user_data.password != user_data.confirm_password:
        return RedirectResponse(
            "/auth/register/?error=Пароли+не+совпадают!",
            status_code=303
        )
    # Хешируем пароль
    user_dict['password'] = auth.get_password_hash(user_data.password)
    # Добавляем нового пользователя
    user = await UsersDAO.add(**user_dict)

    # Создаем ему токен
    access_token = auth.create_access_token({"sub": str(user.id), "email": user.email})
    # Добавляем токен в cookie
    # Также запрещаем доступ к cookie через JavaScript ради безопасности
    response = RedirectResponse(
        url="/main/?success=Вы+успешно+зарегистрированы!", 
        status_code=303
    )
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return response


#=========================================================
# Маршрут /auth/login/
#=========================================================

@router.post("/login/")
async def auth_user(
    response: Response,
    email: EmailStr = Form(...),
    password: str = Form(...)
) -> dict:
    """ Функция для авторизации пользователя """
    user_data = SUserAuth(
        email=email,
        password=password
    )
    # Ищем пользователя
    user = await auth.authenticate_user(email=user_data.email, password=user_data.password)
    
    if user is None:
        return RedirectResponse(
            url="/auth/login/?error=Неверная+почта+или+пароль.",
            status_code=303
        )

    access_token = auth.create_access_token({"sub": str(user.id), "email": user.email})
    response = RedirectResponse(url="/main/", status_code=303)
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return response


#=========================================================
# Маршрут /auth/logout/
#=========================================================

@router.get("/logout/")
async def logout_user(response: Response):
    """ Функция для разлогинивания пользователя """
    # Удаляем токен пользователя
    response = RedirectResponse(url='/auth/login/', status_code=303)
    response.delete_cookie(key="users_access_token")
    return response

#=========================================================
# Маршрут /auth/del/
#=========================================================

# delete обозначает, что функция удаляет данные с сервера
@router.post("/del/")
async def dell_user(request: Request):
    """ Функция для удаления пользователя """
    token = request.cookies.get("users_access_token")
    if not token:
        return RedirectResponse(
            url="/main/?error=Возникла+проблема+при+удалении+аккаунта.",
            status_code=303
        )
    user_data = auth.decode_access_token(token)
    # Ищем пользователя
    user = await UsersDAO.find_one_or_none(email=user_data.get("email"))
    # Если пользователя нет, то ошибка
    if user is None:
        return RedirectResponse(
            url="/main/?error=Возникла+проблема+при+удалении+аккаунта.",
            status_code=303
        )

    # Удаляем пользователя и его токен
    check = await UsersDAO.delete(email=user_data.get('email'))
    response = RedirectResponse(
        url='/auth/login/?success=Удаление+прошло+успешно!', 
        status_code=303
    )
    if check:
        response.delete_cookie(key="users_access_token")
    return response
    