from database.base_class import Base
from sqlalchemy.sql.sqltypes import DateTime, SmallInteger
from sqlalchemy import Column, Integer, String

class Video(Base):
    __tablename__ = 'video'
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    project_id = Column(Integer)
    video_name = Column(String)
    video_type = Column(String)
    s3_url = Column(String)
    created_at = Column(DateTime)
    active = Column(SmallInteger, default=1)