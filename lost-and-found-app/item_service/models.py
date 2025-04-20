from sqlalchemy import Column, Integer, String, Date, DateTime
from database import Base
from datetime import datetime, timezone

# ✅ Item 表
class Item(Base):
    __tablename__ = "items"
    __table_args__ = {"extend_existing": True}  # 防止重复定义错误

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    location = Column(String)
    date = Column(Date)
    type = Column(String, default="lost")  # 可选值：lost / found
    reported_by = Column(String)
    image = Column(String, nullable=True)  # ✅ 上传图片的字段

# ✅ Comment 表
class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, index=True)  # 外键关联 Item.id（此处未设置外键约束）
    content = Column(String)
    commenter = Column(String)
    time = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # ✅ 使用 timezone-aware 时间

