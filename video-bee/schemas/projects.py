from pydantic import BaseModel, json
from typing import List, Optional

class ProjectSchemas(BaseModel):
    project_name: Optional[str]
    user_id: Optional[int]
    project_information: Optional[str]
    s3_url: Optional[str]
    class Config:
        orm_mode = True

class ProjectEdit(BaseModel):
    start_time: int
    end_time: int
    s3_url: str
    video_name: str

class UpdateColumnRequest(BaseModel):
    pid: Optional[int]
    pname: Optional[str]
    user_id: Optional[int]
    s3_url: Optional[str]
    metadata: Optional[str]
