from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 👉 替换为你自己的数据库配置
DATABASE_URL = "postgresql://postgres:252436710@localhost:5432/lostfound"

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建数据库会话
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# 创建基础类用于表模型继承
Base = declarative_base()
