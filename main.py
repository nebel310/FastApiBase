from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from router import router_task as tasks_router
from router import router_user as users_router

# Асинхронный контекстный менеджер для управления жизненным циклом приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print('База очищена')
    await create_tables()
    print('База готова к работе')
    yield
    print('Выключение')

# Создание FastAPI приложения
app = FastAPI(lifespan=lifespan)

# Кастомная OpenAPI схема для Swagger UI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    # Генерация стандартной OpenAPI схемы
    openapi_schema = get_openapi(
        title="Your App",
        version="1.0.0",
        description="API for tasks",
        routes=app.routes,
    )
    
    # Добавляем поддержку Bearer Token в Swagger UI
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    # Указываем, что только маршрут /tasks требует авторизации
    if "/tasks" in openapi_schema["paths"]:
        openapi_schema["paths"]["/tasks"]["get"]["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Применяем кастомную OpenAPI схему
app.openapi = custom_openapi

# Подключаем роутеры
app.include_router(tasks_router)
app.include_router(users_router)