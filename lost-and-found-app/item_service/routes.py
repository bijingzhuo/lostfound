from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Item,Comment
from pydantic import BaseModel
from datetime import date
from auth_proxy import verify_token
from datetime import datetime, timezone
from fastapi import Path
from fastapi import File, UploadFile
import os
router = APIRouter()


class ItemIn(BaseModel):
    name: str
    description: str
    location: str
    date: date
    type: str  # "lost" or "found"
    image: str = None 



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/report")
def report_item(item: ItemIn, authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = authorization.replace("Bearer ", "").strip()
    username = verify_token(token)

    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    new_item = Item(
        name=item.name,
        description=item.description,
        location=item.location,
        date=item.date,
        type=item.type,
        reported_by=username,
        image=item.image
    )

    db.add(new_item)
    db.commit()
    return {"message": "Item reported", "reported_by": username}


@router.get("/items")
def get_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return {
        "items": [
            {
                "id": i.id,
                "name": i.name,
                "description": i.description,
                "location": i.location,
                "date": i.date,
                "reported_by": i.reported_by,
                "type": i.type, 
                "image": i.image
            }
            for i in items
        ]
    }


@router.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter_by(id=item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

class CommentIn(BaseModel):
    content: str

@router.get("/items/{item_id}/comments")
def get_comments(item_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter_by(item_id=item_id).order_by(Comment.time.desc()).all()
    return {
        "comments": [
            {
                "id": c.id,
                "content": c.content,
                "commenter": c.commenter,
                "time": c.time
            }
            for c in comments
        ]
    }


@router.post("/items/{item_id}/comments")
def add_comment(
    item_id: int,
    comment: CommentIn,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = authorization.replace("Bearer ", "").strip()
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    new_comment = Comment(
        item_id=item_id,
        content=comment.content,
        commenter=username,
        time=datetime.now(timezone.utc)
    )

    db.add(new_comment)
    db.commit()
    return {"message": "Comment added", "commenter": username}


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}


@router.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = authorization.replace("Bearer ", "").strip()
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    item = db.query(Item).filter_by(id=item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item.reported_by != username:
        raise HTTPException(status_code=403, detail="Not allowed to delete others' posts")

    db.delete(item)
    db.commit()
    return {"message": "Item deleted"}


class ItemUpdate(BaseModel):
    name: str
    description: str
    location: str
    date: date
    type: str
    image: str = None

@router.put("/items/{item_id}")
def update_item(item_id: int, item: ItemUpdate, authorization: str = Header(None), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "").strip()
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    existing = db.query(Item).filter_by(id=item_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Item not found")
    if existing.reported_by != username:
        raise HTTPException(status_code=403, detail="Not authorized to update this item")

    for field, value in item.dict().items():
        setattr(existing, field, value)

    db.commit()
    return {"message": "Item updated"}


class CommentUpdate(BaseModel):
    content: str

@router.put("/items/{item_id}/comments/{comment_id}")
def update_comment(
    item_id: int,
    comment_id: int,
    updated: CommentUpdate,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    token = authorization.replace("Bearer ", "").strip()
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    comment = db.query(Comment).filter_by(id=comment_id, item_id=item_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.commenter != username:
        raise HTTPException(status_code=403, detail="Not allowed to edit others' comments")

    comment.content = updated.content
    db.commit()
    return {"message": "Comment updated"}


@router.delete("/items/{item_id}/comments/{comment_id}")
def delete_comment(
    item_id: int,
    comment_id: int,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    token = authorization.replace("Bearer ", "").strip()
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    comment = db.query(Comment).filter_by(id=comment_id, item_id=item_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.commenter != username:
        raise HTTPException(status_code=403, detail="Not allowed to delete others' comments")

    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted"}
