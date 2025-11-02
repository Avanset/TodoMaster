from fastapi import FastAPI
from .database import Base, engine
from . import modeles
from .routers import groups

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Task Note')
app.include_router(groups.router)

@app.get('/')
def root():
    return {"ok": True, "message": "Task Note API is running."}