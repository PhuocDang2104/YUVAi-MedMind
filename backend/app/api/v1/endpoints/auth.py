from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import Token, UserCreate, UserLogin

router = APIRouter()


@router.post("/register", response_model=Token)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> Token:
    # TODO: add password hashing, persistence, email validation
    dummy_token = "dev-register-token"
    return Token(access_token=dummy_token)


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> Token:
    # TODO: verify credentials against DB
    if payload.email == "" or payload.password == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    dummy_token = "dev-login-token"
    return Token(access_token=dummy_token)
