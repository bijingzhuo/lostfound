from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from auth import create_token, verify_token
from pydantic import BaseModel

user_router = APIRouter()

# 表单数据格式定义
class UserIn(BaseModel):
    username: str
    password: str

# 获取数据库会话（依赖注入）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 注册接口
@user_router.post("/register")
def register(user: UserIn, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    if db.query(User).filter_by(username=user.username).first():
        raise HTTPException(status_code=400, detail="User already exists")
    
    # 创建新用户
    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    return {"message": "Registered successfully"}

# 登录接口
@user_router.post("/login")
def login(user: UserIn, db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(username=user.username).first()
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(user.username)
    return {"token": token}

# token 验证接口（供其他服务调用）
@user_router.get("/validate")
def validate(token: str):
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": username}
