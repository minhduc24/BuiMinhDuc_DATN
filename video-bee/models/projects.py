from fastapi import HTTPException
from sqlalchemy.orm import Session, exc
from database.entities.project import Project
from models.videos import get_video_by_pid
from schemas.projects import ProjectSchemas, UpdateColumnRequest
from datetime import date, datetime
import json
from sqlalchemy import asc
def get_project_by_uid(db: Session, user_id: int):
    query = db.query(Project).filter(Project.user_id == user_id, Project.active == 1)
    projects = query.order_by(asc(Project.id)).all()
    return projects
def create_new_project(db: Session, project: ProjectSchemas):
    projectInstance = Project(
        project_name = project.project_name,
        user_id = project.user_id,
        project_information = project.project_information,
        s3_url = project.s3_url,
        created_at=date.today().strftime("%d/%m/%Y")
    )
    db.add(projectInstance)
    db.commit()
    db.refresh(projectInstance)
    return projectInstance

def update_active_column_project(db: Session, project_id: int):
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return {"message": "not found"}
        project.active = 0
        db.commit()
        return {"message": " updated successfully"}
    except exc.SQLAlchemyError as e:
        db.rollback()
        return {"message": str(e)}
    finally:
        db.close()

def save_projectt(db: Session, request: UpdateColumnRequest):
    project = db.query(Project).filter(Project.id == request.pid).first()
    setattr(project, 'modified_at', datetime.now())
    if not project:
        raise HTTPException(status_code=404, detail='Record not found')
    if request.pname:
        setattr(project, 'project_name', request.pname)
    if request.s3_url:
        setattr(project, 's3_url', request.s3_url)
    if request.user_id:
        setattr(project, 'user_id', request.user_id)
    if request.metadata:
        metadata_json = request.metadata
        setattr(project, 'project_information', metadata_json)

    db.commit()
    return {'message': 'Column updated successfully'}

def get_p_by_id(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    videos = get_video_by_pid(db, project_id)
    return {
        "project": project,
        "videos": videos
    }