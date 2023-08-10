from database.base_class import Base
from sqlalchemy.sql.sqltypes import DateTime, SmallInteger
from sqlalchemy import Column, Integer, String
from email.policy import default

def imageDefault():
	src = "https://www.kindpng.com/imgv/iwoxbb_user-profile-default-image-png-clipart-png-download/"
	return src


class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
	name = Column(String)
	password = Column(String)
	mail = Column(String)
	image = Column(String, default=imageDefault())
	registration_date = Column(DateTime)
	active = Column(SmallInteger, default=1)