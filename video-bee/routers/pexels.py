from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from database.database import SessionLocal
from models.pexels import *
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post('/pexels')
async def post_render(request: Request):
    data  = await request.json()
    try:
        reply = submit(data)

        return JSONResponse({
            "status":   "success",
            "message":  "OK",
            "data":     {
                "id":       reply.id,
                "message":  reply.message
            }
        })
    except Exception as e:
        print(44444)
        return {
            "status":   "fail",
            "message":  "Bad Request",
            "data":     e
        }

@router.get('/pexels/{renderId}')
def render(renderId):
    try:
        reply = status(renderId).to_dict()

        return JSONResponse({
            "status":   "success",
            "message":  "OK",
            "data":     {
                "data":     reply.get('data', None),
                "status":   reply.get('status', None),
                "url":      reply.get('url', None)
            }
        })
    except Exception as e:
        return JSONResponse({
            "status":   "fail",
            "message":  "Bad Request",
            "data":     e
        })