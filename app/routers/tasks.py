from fastapi import APIRouter, Depends, HTTPException, Response, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..database import get_db
from .. import modeles, schemas

router = APIRouter(prefix='/tasks', tags=['tasks'])

@router.get('/', response_model=list[schemas.TaskRead])
def list_tasks(group_id: int | None = Query(default=None,description='このグループIDで絞り込み'),db: Session = Depends(get_db)):
    
    stmt = select(modeles.Task)
    
    if group_id is not None:
        stmt = stmt.where(modeles.Task.group_id == group_id)
    
    stmt = stmt.order_by(modeles.Task.order.asc(), modeles.Task.id.asc())
    return db.scalars(stmt).all()

@router.post('/', response_model=schemas.TaskRead, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    
    # グループIDが指定されている場合、そのグループが存在するか確認
    if task.group_id is not None and db.get(modeles.TaskGroup, task.group_id) is None:
        raise HTTPException(status_code=400, detail='指定されたグループが存在しません。')
    
    t = modeles.Task(**task.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

@router.get('/{task_id}', response_model=schemas.TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    t = db.get(modeles.Task, task_id)
    
    if not t:
        raise HTTPException(status_code=404, detail='Task not found')
    return t


@router.patch('/{task_id}', response_model=schemas.TaskRead)
def update_task(task_id: int, patch: schemas.TaskUpdate, db: Session = Depends(get_db)):
    t = db.get(modeles.Task, task_id)
    
    if not t:
        raise HTTPException(status_code=404, detail='Task not found')
    
    data = patch.model_dump(exclude_none=True)
    
    # グループIDが指定されている場合、そのグループが存在するか確認
    if 'group_id' in data and data['group_id'] is not None:
        if db.get(modeles.TaskGroup, data['group_id']) is None:
            raise HTTPException(status_code=400, detail='指定されたグループが存在しません。')
        
    for key, value in data.items():
        setattr(t,key,value)
    db.commit()
    db.refresh(t)
    return t

@router.delete('/{task_id}', status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    t = db.get(modeles.Task, task_id)
    
    if not t:
        raise HTTPException(status_code=404, detail='Task not found')
    
    db.delete(t)
    db.commit()
    
    return Response(status_code=204)