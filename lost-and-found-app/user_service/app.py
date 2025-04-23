
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import user_router
from database import Base, engine

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(user_router)

