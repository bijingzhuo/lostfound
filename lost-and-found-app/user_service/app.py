
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import user_router
from database import Base, engine

app = FastAPI()

# ✅ 加入跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有前端地址请求，正式环境可改为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(user_router)

