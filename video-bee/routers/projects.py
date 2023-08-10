from fastapi import APIRouter, Depends, HTTPException
from models.projects import *
from schemas.projects import ProjectSchemas, ProjectEdit, UpdateColumnRequest
from database.database import SessionLocal
from schemas.videos import VideoSchemas
from models.shotstack import *

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/projects/{project_id}")
async def get_project_by_id(project_id: int, db: Session = Depends(get_db)):
    return get_p_by_id(db, project_id)

@router.get("/projects")
async def get_project_by_user_id(user_id: int, db: Session = Depends(get_db)):
    project = get_project_by_uid(db, user_id)
    return project
@router.post("/projects")
async def create_nproject(project: ProjectSchemas, db: Session = Depends(get_db)):
    return create_new_project(db, project)

@router.post("/projects/edit")
async def create_project(edit_infor: dict, db: Session = Depends(get_db)):
    print(edit_infor)
    return download_file(edit_infor, db)

@router.patch("/projects/{project_id}")
async def update_project(project_id: int, db: Session = Depends(get_db)):
    return update_active_column_project(db, project_id)

@router.put("/projects/{project_id}")
async def save_project(request: UpdateColumnRequest, db: Session = Depends(get_db)):
    return save_projectt(db, request)