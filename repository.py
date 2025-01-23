from database import new_session, TasksOrm
from schemas import STaskAdd, STask
from sqlalchemy import select, cast, Integer


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()
            
            task = TasksOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id
    
    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TasksOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [STask.model_validate(task_model) for task_model in task_models]
            return task_schemas
    
    @classmethod
    async def get_one(cls, task_id: int) -> STask | None:
        async with new_session() as session:
            query = select(TasksOrm).where(TasksOrm.id == cast(task_id, Integer))
            result = await session.execute(query)
            task_model = result.scalars().first()
            if task_model:
                return STask.model_validate(task_model)
            return None
    
    @classmethod
    async def delete_one(cls, task_id: int) -> bool:
        async with new_session() as session:
            query = select(TasksOrm).where(TasksOrm.id == cast(task_id, Integer))
            result = await session.execute(query)
            task_model = result.scalars().first()
            if task_model:
                await session.delete(task_model)
                await session.commit()
                return True
            return False