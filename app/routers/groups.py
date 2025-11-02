from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..database import get_db
from .. import modeles, schemas

router = APIRouter(prefix='/groups', tags=['groups'])

@router.get('/',response_model=list[schemas.GroupRead])
def list_groups(db: Session = Depends(get_db)):
    stmt = select(modeles.TaskGroup).order_by(modeles.TaskGroup.id.asc())
    return db.scalars(stmt).all()

@router.post('/', response_model=schemas.GroupRead, status_code=201)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    g = modeles.TaskGroup(**group.model_dump())
    db.add(g)
    db.commit()
    db.refresh(g)
    
    return g

@router.get('/{group_id}', response_model=schemas.GroupRead)
def get_group(group_id: int, db: Session = Depends(get_db)):
    g = db.get(modeles.TaskGroup, group_id)
    if not g:
        raise HTTPException(status_code=404,detail='Group not found') 
    return g   