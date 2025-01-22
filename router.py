from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from security import create_access_token, get_current_user
from schemas import STaskAdd, STask, STaskId, SUserRegister
from typing import Annotated
from repository import TaskRepository, UserRepository
from database import UserOrm


router_task = APIRouter(
    prefix="/tasks",
    tags=['Задачи']
)

router_user = APIRouter(
    prefix="/auth",
    tags=['Пользователи']
)


@router_task.post('')
async def add_task(
    task: Annotated[STaskAdd, Depends()]
) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return {'success': True, 'task_id': task_id}


@router_task.get("", response_model=list[STask], dependencies=[Depends(get_current_user)])
async def get_tasks(current_user: UserOrm = Depends(get_current_user)):
    tasks = await TaskRepository.find_all()
    return tasks


@router_task.get('/{task_id}', response_model=STask)
async def get_task(task_id: int) -> STask | None:
    task = await TaskRepository.get_one(task_id)
    if task:
        return task
    raise HTTPException(status_code=404, detail=f'id {task_id} не существует')


@router_task.delete('{task_id}')
async def delete_task(task_id: int):
    is_deleted = await TaskRepository.delete_one(task_id)
    if is_deleted:
        return {'success': True, 'message': 'Задача с id {task_id} удалена'}
    raise HTTPException(status_code=404, detail='Задача с id {task_id} не найдена')



@router_user.post("/register")
async def register_user(user_data: SUserRegister):
    try:
        user_id = await UserRepository.register_user(user_data)
        return {"success": True, "user_id": user_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router_user.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserRepository.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")
    
    # Создаём токен
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}