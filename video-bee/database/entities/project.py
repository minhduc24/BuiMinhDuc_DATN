from database.base_class import Base
from sqlalchemy.sql.sqltypes import DateTime, SmallInteger
from sqlalchemy import Column, Integer, String

class Project(Base):
    __table_name__ = "project"
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    project_name = Column(String)
    user_id = Column(Integer)
    project_information = Column(String)
    s3_url = Column(String)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)
    active = Column(SmallInteger, default=1)