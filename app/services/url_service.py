from datetime import datetime
from app.models.url import URL
from app.models.analytics import Analytics
from app.core.encoder import encode
from app.cache.redis_client import r



def create_short_url(
    db,
    long_url: str,
    custom_code: str = None,
    user_id: int = None,
    expires_at=None
):
    long_url = str(long_url)

    # ✅ Custom alias case
    if custom_code:
        existing = db.query(URL).filter(URL.short_code == custom_code).first()
        if existing:
            raise Exception("Custom code already exists")

        new_url = URL(
            long_url=long_url,
            short_code=custom_code,
            user_id=user_id,
            expires_at=expires_at
        )

        db.add(new_url)
        db.commit()

        # cache
        r.set(custom_code, long_url, ex=86400)

        return custom_code

    
    new_url = URL(
        long_url=long_url,
        user_id=user_id,
        expires_at=expires_at
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    short_code = encode(new_url.id)

    new_url.short_code = short_code
    db.commit()

    # cache
    r.set(short_code, long_url, ex=86400)

    return short_code



def get_long_url(db, code: str):
    # Step 1: Redis cache
    cached = r.get(code)
    if cached:
        return cached

    # Step 2: DB lookup
    url = db.query(URL).filter(URL.short_code == code).first()

    if not url:
        return None

    # Step 3: Expiry check
    if url.expires_at and url.expires_at < datetime.utcnow():
        return None

    # Step 4: Cache result
    r.set(code, url.long_url, ex=86400)

    return url.long_url



def get_click_stats(db, code: str):
    return db.query(Analytics).filter(
        Analytics.short_code == code
    ).count()