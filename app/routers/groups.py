from fastapi import APIRouter, Depends, HTTPException,Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..database import get_db
from .. import models, schemas,crud

router = APIRouter(prefix='/groups', tags=['groups'])

@router.get('/',response_model=list[schemas.GroupRead])
def list_groups(db: Session = Depends(get_db)):
    stmt = select(models.TaskGroup).order_by(models.TaskGroup.id.asc())
    return db.scalars(stmt).all()

@router.post('/', response_model=schemas.GroupRead, status_code=201)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    g = models.TaskGroup(**group.model_dump())
    db.add(g)
    db.commit()
    db.refresh(g)
    
    return g

@router.get('/{group_id}', response_model=schemas.GroupRead)
def get_group(group_id: int, db: Session = Depends(get_db)):
    g = db.get(models.TaskGroup, group_id)
    if not g:
        raise HTTPException(status_code=404,detail='Group not found') 
    return g   

@router.patch('/{group_id}', status_code=204)
def update_group(group_id: int, group: schemas.GroupUpdate, db: Session = Depends(get_db)):
    g = db.get(models.TaskGroup, group_id)
    
    if not g:
        raise HTTPException(status_code=404, detail='Group not found')
    for key, value in group.model_dump(exclude_none=True).items():
        setattr(g,key,value)
    db.commit()
    db.refresh(g)
    
    return g

@router.delete('/{group_id}',status_code=204)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    g = db.get(models.TaskGroup, group_id)
    
    if not g:
        raise HTTPException(status_code=404, detail='Group not found')
    
    db.delete(g)
    db.commit()
    
    return Response(status_code=204)

@router.get('/ui', response_class=HTMLResponse)
def groups_ui(request: Request, db: Session = Depends(get_db)):
    groups_ = crud.list_groups(db)
    
    return templates.TemplateResponse('groups.html', {'request' : request, 'groups': groups_})
