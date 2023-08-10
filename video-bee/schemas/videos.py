from pydantic import BaseModel
from typing import List, Optional

class VideoSchemas(BaseModel):
    project_id: Optional[int]
    video_name: Optional[str]
    video_type: Optional[str]
    s3_url: Optional[str]
    class Config:
        orm_mode = True

