from fastapi import FastAPI
from database import Base, engine
from routes import router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
# ✅ 先创建 app 实例
app = FastAPI()

# ✅ 设置 CORS：开发期间允许所有前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 正式上线时建议改为前端具体地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 创建并挂载上传目录（用于图片上传）
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


# ✅ 初始化数据库表
Base.metadata.create_all(bind=engine)

# ✅ 加载业务路由（比如 /report、/items、/comments、/upload-image 等）
app.include_router(router)
