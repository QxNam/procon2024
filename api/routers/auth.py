from fastapi import APIRouter, HTTPException, Depends
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta
from .. import security, schemas
from ..models import User
from ..database import get_async_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register")
async def register_user(data:dict, db: AsyncSession = Depends(get_async_db)):
    username = data.get("username")
    password = data.get("password")
    # Kiểm tra nếu user đã tồn tại
    query = select(User).filter(User.username == username) 
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Tạo user mới
    hashed_password = security.get_password_hash(password) 
    new_user = User(username=username, password=hashed_password)  
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return {"message": "User registered successfully", "user_id": new_user.id}

@router.post("/token", response_model=schemas.Token, status_code=201)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db)
):
    user = await security.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Tạo token với thời gian hết hạn
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )
    
    # Trả về token và thông tin liên quan
    return schemas.Token(token="Bearer "+access_token) 
