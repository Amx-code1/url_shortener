from pydantic import BaseModel, HttpUrl
from typing import Optional
from sqlalchemy import DateTime
from datetime import datetime

expires_at: Optional[datetime] = None

class URLCreate(BaseModel):
    url: HttpUrl
    custom_code: Optional[str] = None