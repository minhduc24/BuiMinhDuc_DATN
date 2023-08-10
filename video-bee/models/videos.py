from sqlalchemy.orm import Session
from database.entities.video import Video
from schemas.videos import VideoSchemas
from datetime import date

def get_video_by_pid(db:Session, pid: int):
    return db.query(Video).filter(Video.project_id == pid, Video.active == 1).all()

def get_video_by_id(db:Session, video_id: int):
    return db.get(Video, video_id)

def create_new_video(db: Session, video: VideoSchemas):
    videoInstance = Video(
        project_id=video.project_id,
        video_name = video.video_name,
        video_type = video.video_type,
        s3_url = video.s3_url,
        created_at=date.today().strftime("%d/%m/%Y")
    )
    db.add(videoInstance)
    db.commit()
    db.refresh(videoInstance)
    return videoInstance

def update_active_video(db: Session, video_id: int):
    video = db.query(Video).filter(Video.id == video_id).first()
    video.active = 0
    db.commit()
    return {"status": "remove thanh cong"}