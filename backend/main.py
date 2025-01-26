from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from chatbot import router as chatbot_router
from database import get_db
from jose import jwt, JWTError
from models import User
from config import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chatbot_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Hello from Chatbot Backend!"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")