from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session,selectinload
from . import models, schemas

#================
# Group CRUD
def list_groups(db: Session) -> List[models.TaskGroup]:
    stmt = select(models.TaskGroup).order_by(models.TaskGroup.id.asc())
    return db.scalars(stmt).all()

def create_group(db: Session, data: schemas.GroupCreate) -> models.TaskGroup:
    group = models.TaskGroup(**data.model_dump())
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

def get_group(db: Session, group_id: int) -> Optional[models.TaskGroup]:
    return db.get(models.TaskGroup, group_id)

def update_group(db: Session, group_id: int, data: schemas.GroupUpdate) -> Optional[models.TaskGroup]:
    group = db.get(models.TaskGroup, group_id)
    if not group:
        return None
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(group, key, value)
    db.commit()
    db.refresh(group)
    return group

def delete_group(db: Session, group_id: int) -> bool:
    group = db.get(models.TaskGroup, group_id)
    if not group:
        return False
    db.delete(group)
    db.commit()
    return True

#================
# Task CRUD
#================
def list_tasks(db: Session, group_id: Optional[int] = None) -> List[models.Task]:
    stmt = select(models.Task).options(selectinload(models.Task.notes)).order_by(models.Task.id.asc())
    if group_id is not None:
        stmt = stmt.where(models.Task.group_id == group_id)
    return db.scalars(stmt).all()

def create_task(db: Session, data: schemas.TaskCreate) -> models.Task:
    task = models.Task(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    return db.get(models.Task, task_id)

def update_task(db: Session, task_id: int, data: schemas.TaskUpdate) -> Optional[models.Task]:
    task = db.get(models.Task, task_id)
    if not task:
        return None
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int) -> bool:
    task = db.get(models.Task, task_id)
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True

#================
# WorkNote CRUD
#================

def list_notes(db: Session, task_id: int) -> List[models.WorkNote]:
    task = db.get(models.Task, task_id)
    if not task:
        return []
    return task.notes

def create_note(db: Session, data: schemas.WorkNoteCreate) -> Optional[models.WorkNote]:
    if db.get(models.Task, data.task_id) is None:
        raise ValueError('Task not found')
    
    note = models.WorkNote(**data.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def update_note(db: Session, note_id: int, data: schemas.WorkNoteUpdate) -> Optional[models.WorkNote]:
    note = db.get(models.WorkNote, note_id)
    if not note:
        return None
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(note, key, value)
    db.commit()
    db.refresh(note)
    return note

def delete_note(db: Session, note_id: int) -> bool:
    note = db.get(models.WorkNote, note_id)
    if not note:
        return False
    db.delete(note)
    db.commit()
    return True