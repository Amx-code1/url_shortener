import os
from datetime import datetime, timedelta

from jose import jwt, JWTError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

#  Safety check (VERY IMPORTANT)
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in environment variables")


#  CREATE TOKEN
def create_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(hours=2)

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


#  VERIFY TOKEN
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except JWTError:
        return None