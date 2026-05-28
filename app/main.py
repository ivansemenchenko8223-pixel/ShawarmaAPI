from fastapi import FastAPI
from app.api.v1.endpoints.router import router 
from app.db.session import engine
from app.db.session import Base
import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)