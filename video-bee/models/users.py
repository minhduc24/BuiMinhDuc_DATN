from sqlalchemy.orm import Session
from database.entities.user import User
from schemas.users import UserSchemas
from datetime import date
from loguru import logger
import boto3
import mimetypes
from config import S3_BUCKET, S3_ACCESS_KEY_ID, S3_SECRET_ACCESS_KEY

s3 = boto3.resource('s3',
                    aws_access_key_id=S3_ACCESS_KEY_ID,
                    aws_secret_access_key=S3_SECRET_ACCESS_KEY)

bucket = s3.Bucket(S3_BUCKET)


# def get_user_by_id(db: Session, user_id: int):
# 	user = db.get(User, user_id)
# 	return user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.mail == email).first()


def create_new_user(db: Session, user: UserSchemas):
    exits_user = get_user_by_email(db, user.email)
    if (exits_user is None):
        userInstance = User(
            name=user.name,
            password=user.password,
            mail=user.email,
            image=user.image,
            registration_date=date.today().strftime("%d/%m/%Y")
        )
        db.add(userInstance)
        db.commit()
        db.refresh(userInstance)
        if userInstance.id is not None:
            return {"status": "Dang ki thanh cong", "type": "success", "user": userInstance}
    return {"status": "Email nay da ton tai", "type": "error"}


async def s3_upload(contents: bytes, key: str):
    mime_type, encoding = mimetypes.guess_type(key)
    if mime_type is None:
        mime_type = 'binary/octet-stream'
    logger.info(f'Uploading {key} to s3')
    extra_args = {
        'ContentType': mime_type
    }
    return bucket.put_object(Key=key, Body=contents, **extra_args)

def update_userr(db: Session, updatee):
    user = db.query(User).filter(User.id == updatee.id).first()
    if user:
        setattr(user, 'name', updatee.name)
        setattr(user, 'mail', updatee.email)
        setattr(user, 'password', updatee.password)
        db.commit()
        return {"message": "OK"}
    else:
        return {"message": "NOK"}