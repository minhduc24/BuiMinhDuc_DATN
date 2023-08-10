from fastapi import APIRouter, UploadFile, status, Form, File
from models.videos import *
from schemas.users import UserUpdate
from database.database import SessionLocal
from uuid import uuid4
from schemas.videos import VideoSchemas
from models.auth import *
from typing import Optional

router = APIRouter()

KB = 1024
MB = 1024 * KB

SUPPORTED_FILE_TYPES = {
    'image/png': 'png',
    'image/jpeg': 'jpg',
    'video/mp4': 'mp4'
}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @router.get("/users/{user_id}", dependencies=[Depends(validate_token)])
# async def get_user(user_id: int, db: Session = Depends(get_db)):
#     user = get_user_by_id(db, user_id)
#     return user

@router.get("/users")
async def get_user_mail(email: str , db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)
    return user

@router.post("/users")
async def create_user(user: UserSchemas, db: Session = Depends(get_db)):
    return create_new_user(db, user)

# @router.post("/videos")
# async def create_vieo(video: VideoSchemas, db: Session = Depends(get_db)):
#     return create_new_video(db, video)


@router.post("/uploads")
async def upload(pid: int = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No file found!!'
        )
    contents = await file.read()
    size = len(contents)

    if not 0 < size <= 50 * MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Supported file size is 0 - 50 MB'
        )

    file_name = f'{uuid4()}{file.filename}'
    s3_result = await s3_upload(contents=contents, key=file_name)

    [file_name, file_type] = file.filename.split(".")
    videoInstance = Video
    Video.video_name = file_name
    Video.s3_url = f"https://videoaws.s3.ap-southeast-1.amazonaws.com/{s3_result.key}"
    Video.project_id = pid,
    Video.video_type = file_type,
    return create_new_video(db, videoInstance)


@router.put("/users/{user_id}")
def update_user(user_update: UserUpdate, db: Session = Depends(get_db)):
    return update_userr(db, user_update)
