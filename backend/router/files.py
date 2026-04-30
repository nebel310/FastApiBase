from fastapi import(
    APIRouter, Depends, HTTPException,
    UploadFile, status, File,
    Form
)

from minio.exceptions import StorageError, ObjectNotFoundError
from schemas.base import ErrorResponse, ValidationErrorResponse
from schemas.files import SFileResponse
from models.auth import UserOrm
from repositories.files import FileRepository
from utils.security import get_current_user




router = APIRouter(
    prefix="/files",
    tags=['Файлы']
)



@router.post(
    "/",
    response_model=SFileResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ValidationErrorResponse, "description": "Ошибка валидации"},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
        502: {"model": ErrorResponse, "description": "Ошибка связи с S3-хранилищем"},
    }
)
async def upload_file(
    file: UploadFile,
    current_user: UserOrm = Depends(get_current_user)
):
    """
    Загружает файл в облачное хранилище
    """
    try:
        file_bytes = await file.read()
    except Exception:
        raise HTTPException(status_code=400, detail="Ошибка чтения файла")

    try:
        file_data = await FileRepository.upload_file(
            file_bytes=file_bytes,
            original_name=file.filename,
            uploaded_by=current_user.id,
        )
        return file_data

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except StorageError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")
    

""" 
TODO:

Доделать эндпоинты скачивания и удаления файлов

Добавить пользователю поле "avatar_id"
Создать эндпоинт по применению аватара с автозаменой и удалением
*ну подумать по лучше как бы улушить логику с аватаркой и работой с файлами*

Реализовать эндпоинт по получению всех пользователей с cursor пагинацией
"""