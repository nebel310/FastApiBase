from pydantic import BaseModel, ConfigDict
from enum import Enum


class STaskAdd(BaseModel):
    name: str
    description: str | None = None


class STask(STaskAdd):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class STaskId(BaseModel):
    ok: bool = True
    task_id: int


class SUserAuth(BaseModel):
    username: str
    password: str


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class SUserRegister(SUserAuth):
    password_confirm: str
    role: UserRole = UserRole.USER  # Добавляем поле role