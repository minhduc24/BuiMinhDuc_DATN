from sqlalchemy.orm.session import Session
from i18n import t

from utils.exceptions import Unauthorized
from entities.user import User
from models.users import Users
from utils.log import log

class ServiceAuth:
	@classmethod
	def login(cls, login_code: str, db: Session):
		"""
		Get Access Token and Refresh Token
		:param login_code:
		:param db:
		:param authorize:
		:return:
		"""
		user = cls.get_current_user(login_code, db)
		return {
			"user_code": user.user_code,
			"user_info": {
				"user_id": user.id,
				"created_at": user.created_at,
				"created_by": user.created_by
			}
		}

	@classmethod
	def get_current_user(cls, login_code: str, db: Session):
		user = db.query(User).filter(User.login_code == login_code, User.active == Users.ACTIVE).first()
		if user is None:
			raise Unauthorized(t("common.errors.auth.bad_login_code"))
		# add log
		log('login', {"user_code": login_code})
		return user