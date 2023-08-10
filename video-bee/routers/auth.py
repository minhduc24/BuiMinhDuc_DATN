from fastapi import APIRouter, Depends
from schemas.auth import LoginRequest
from models.auth import *
from database.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post('/login')
async def login(request_data: LoginRequest, db: Session= Depends(get_db)):
     user = verify_password(request_data.email, request_data.password, db)
     if user is not None and user is not False:
        token = generate_token(request_data.email)
        return {
            'message': 'thanh cong',
            'token': token,
            'user': user
        }
     return {
         'message': 'ten tai khoan hoac mat khau khong dung'
     }
