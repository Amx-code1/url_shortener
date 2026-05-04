import pytest
from datetime import datetime, timedelta

from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.models.url import URL
from app.services.url_service import create_short_url, get_long_url

#  Create tables once before tests run
Base.metadata.create_all(bind=engine)


#  Fixture: clean DB before each test
@pytest.fixture
def db():
    db = SessionLocal()

    # Clear existing data
    db.query(URL).delete()
    db.commit()

    yield db

    db.close()


#  Test: create short URL
def test_create_short_url(db):
    code = create_short_url(db, "https://google.com")

    assert code is not None
    assert isinstance(code, str)


#  Test: duplicate custom code
def test_duplicate_custom_code(db):
    create_short_url(db, "https://google.com", custom_code="test123")

    with pytest.raises(Exception):
        create_short_url(db, "https://google.com", custom_code="test123")


#  Test: retrieve original URL
def test_get_long_url(db):
    code = create_short_url(db, "https://example.com")

    url = get_long_url(db, code)

    assert url == "https://example.com"


#  Test: expired URL should return None
def test_expired_url(db):
    code = create_short_url(
        db,
        "https://expired.com",
        expires_at=datetime.utcnow() - timedelta(hours=1)
    )

    url = get_long_url(db, code)

    assert url is None