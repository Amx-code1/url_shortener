from app.cache.redis_client import r
import time
from fastapi import HTTPException
from fastapi import APIRouter, Depends
from fastapi import Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from app.db.session import SessionLocal
from app.schemas.url import URLCreate
from app.services.url_service import (
    create_short_url,
    get_long_url,
    get_click_stats
)
from app.queue.redis_queue import push_event
from app.core.logger import logger
from app.core.auth import create_token
from app.core.deps import get_current_user
from app.models.url import URL

router = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def rate_limit(ip: str):
    key = f"rate:{ip}"
    requests = r.get(key)

    if requests and int(requests) > 10:
        return False

    r.incr(key)
    r.expire(key, 60)  # 1 minute window

    return True

@router.post("/shorten")
def shorten(
    request: Request,
    body: URLCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    ip = request.client.host

    if not rate_limit(ip):
        return {"error": "Too many requests"}

    try:
        code = create_short_url(
            db,
            str(body.url),
            body.custom_code,
            user_id=user["user_id"]   
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"short_url": f"http://localhost:8000/{code}"}

@router.post("/login")
def login():
    token = create_token({"user_id": 1})
    return {"access_token": token}


@router.get("/stats/{code}")
def stats(code: str, db: Session = Depends(get_db)):
    clicks = get_click_stats(db, code)
    return {"short_code": code, "clicks": clicks}

@router.get("/my-urls")
def my_urls(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    urls = db.query(URL).filter(URL.user_id == user["user_id"]).all()

    return [
        {
            "short_code": u.short_code,
            "long_url": u.long_url
        }
        for u in urls
    ]


@router.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    try:
        url = get_long_url(db, code)

        if not url:
            return {"error": "Not found"}

        push_event(code)

        return RedirectResponse(url)

    except Exception as e:
        logger.error(f"Redirect error: {str(e)}")
        return {"error": "Internal server error"}
    


@router.get("/analytics/{code}")
def analytics(code: str, db: Session = Depends(get_db)):
    clicks = get_click_stats(db, code)

    return {
        "short_code": code,
        "clicks": clicks
    }

