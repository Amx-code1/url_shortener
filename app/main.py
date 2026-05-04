from fastapi import FastAPI
from app.api.routes import router
from app.db.base import Base
from app.db.session import engine

# import models so tables get created
from app.models.url import URL
from app.models.analytics import Analytics

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "running"}