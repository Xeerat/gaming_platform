from pathlib import Path
from sys import path

# Добавляем корень проекта в пути, для нормальной работы импо
path_to_root = str(Path(__file__).parent.parent)
path.append(path_to_root)

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# Файл где определены маршруты для работы с пользователями
# Маршрут это связь между url и функцией
# Он отвечает за то какая функция будет выполняться, после перехода по url
from users.router import router as router_users

# Создаем объект для работы с http-запросами
app = FastAPI()

# Подключаем все маршруты пользователя к главному объекту 
app.include_router(router_users)

app.mount('/static', StaticFiles(directory="site/static"), name="static")

templates = Jinja2Templates(directory="site/templates")

@app.get("/auth/register/", response_class=HTMLResponse)
async def register(request: Request, error: str = None):
    return templates.TemplateResponse('register.html', {
        "request": request,
        "error": error
    })

@app.get("/auth/login/", response_class=HTMLResponse)
async def login(request: Request, success: str = None, error: str = None):
    return templates.TemplateResponse('login.html', {
        "request": request,
        "success": success,
        "error": error
    })

@app.get("/auth/register/terms", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse('terms_use.html', {"request": request})

@app.get("/main/", response_class=HTMLResponse)
async def main_paper(request: Request, success: str = None, error: str = None):
    return templates.TemplateResponse('main_page.html', {
        "request": request,
        "success": success,
        "error": error
    })