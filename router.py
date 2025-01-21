from fastapi import APIRouter, Depends
from schemas import STaskAdd, STask, STaskId
from typing import Annotated
from repository import TaskRepository


router = APIRouter(
    prefix="/tasks",
    tags=['Задачи']
)


@router.post('')
async def add_task(
    task: Annotated[STaskAdd, Depends()]
) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return {'success': True, 'task_id': task_id}


@router.get('')
async def get_tasks() -> STask:
    tasks = await TaskRepository.find_all()
    return tasks