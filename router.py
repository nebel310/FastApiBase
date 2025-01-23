from fastapi import APIRouter, Depends, HTTPException
from schemas import STaskAdd, STask, STaskId
from typing import Annotated
from repository import TaskRepository


router_task = APIRouter(
    prefix="/tasks",
    tags=['Задачи']
)

router_users = APIRouter(
    prefix="/users",
    tags=['Пользователи']
)


@router_task.post('')
async def add_task(
    task: Annotated[STaskAdd, Depends()]
) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return {'success': True, 'task_id': task_id}


@router_task.get('')
async def get_tasks() -> list[STask]:
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