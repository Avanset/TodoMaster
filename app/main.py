from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models
from .routers import groups,tasks,notes
from . import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Task Note')

app.mount('/static', StaticFiles(directory='app/static'), name='static')
templates = Jinja2Templates(directory='app/templates')

app.include_router(groups.router)
app.include_router(tasks.router)
app.include_router(notes.router)

@app.get('/',response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    groups_ = crud.list_groups(db)
    tasks_ = crud.list_tasks(db)
    
    return templates.TemplateResponse('index.html',{
        'request': request, 'groups': groups_, 'tasks': tasks_
    },)
    
@app.get('/ui/groups', response_class=HTMLResponse)
def groups_ui(request: Request, db: Session = Depends(get_db)):
    groups_ = crud.list_groups(db)
    
    return templates.TemplateResponse('groups.html', {'request' : request, 'groups': groups_})

@app.get('/ui/tasks', response_class=HTMLResponse)
def tasks_ui(request: Request, group_id: int | None = None, db: Session = Depends(get_db)):
    groups_ = crud.list_groups(db)
    tasks_ = crud.list_tasks(db,group_id=group_id)
    
    return templates.TemplateResponse('tasks.html', {
        'request' : request, 'groups': groups_, 'tasks': tasks_, 'group_id': group_id
    })
    
@app.get('/ui/tasks/{task_id}/detail', response_class=HTMLResponse)
def task_detail(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id=task_id)
    
    if not task:
        return HTMLResponse('Task not found', status_code=404)
    
    groups_ = crud.list_groups(db)
    
    return templates.TemplateResponse('task_detail.html', {
        'request' : request, 'task': task, 'groups': groups_})