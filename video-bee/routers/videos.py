from fastapi import APIRouter, Depends, HTTPException
from database.database import SessionLocal
from models.videos import *
from schemas.videos import VideoSchemas


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/videos/{video_id}")
async def get_video(video_id: int, db: Session = Depends(get_db)):
    return get_video_by_id(db, video_id)

@router.get("/videos")
async def get_video_by_project_id(pid: int, db: Session = Depends(get_db)):
    return get_video_by_pid(db, pid)

@router.post("/videos")
async def create_video(video: VideoSchemas, db: Session = Depends(get_db)):
    return create_new_video(db, video)

@router.patch("/videos/{video_id}")
async def update_video(video_id: int, db: Session = Depends(get_db)):
    return update_active_video(db, video_id)