from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from router import router_task as tasks_router
from router import router_user as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print('База очищена')
    await create_tables()
    print('База готова к работе')
    yield
    print('Выключение')

app = FastAPI(lifespan=lifespan)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Your App",
        version="1.0.0",
        description="API for tasks",
        routes=app.routes,
    )
    
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
        openapi_schema["paths"]["/tasks"]["post"]["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(tasks_router)
app.include_router(users_router)