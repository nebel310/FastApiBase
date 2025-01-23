from database import new_session, TaskOrm, UserOrm
from schemas import STaskAdd, STask, SUserRegister
from sqlalchemy import select, cast, Integer
from passlib.context import CryptContext


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()
            
            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id
    
    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [STask.model_validate(task_model) for task_model in task_models]
            return task_schemas
    
    @classmethod
    async def get_one(cls, task_id: int) -> STask | None:
        async with new_session() as session:
            query = select(TaskOrm).where(TaskOrm.id == cast(task_id, Integer))
            result = await session.execute(query)
            task_model = result.scalars().first()
            if task_model:
                return STask.model_validate(task_model)
            return None
    
    @classmethod
    async def delete_one(cls, task_id: int) -> bool:
        async with new_session() as session:
            query = select(TaskOrm).where(TaskOrm.id == cast(task_id, Integer))
            result = await session.execute(query)
            task_model = result.scalars().first()
            if task_model:
                await session.delete(task_model)
                await session.commit()
                return True
            return False



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    @classmethod
    async def register_user(cls, user_data: SUserRegister) -> int:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.username == user_data.username)
            result = await session.execute(query)
            if result.scalars().first():
                raise ValueError("Пользователь с таким логином уже существует")
            
            hashed_password = pwd_context.hash(user_data.password)
            
            user = UserOrm(
                username=user_data.username,
                hashed_password=hashed_password,
                role=user_data.role
            )
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id
    
    @classmethod
    async def authenticate_user(cls, username: str, password: str) -> UserOrm | None:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.username == username)
            result = await session.execute(query)
            user = result.scalars().first()
            
            if not user or not pwd_context.verify(password, user.hashed_password):
                return None
            
            return user
    
    @classmethod
    async def get_user_by_username(cls, username: str) -> UserOrm | None:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.username == username)
            result = await session.execute(query)
            return result.scalars().first()