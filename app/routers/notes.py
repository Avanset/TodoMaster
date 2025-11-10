from fastapi import APIRouter, Depends, HTTPException, Response, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..database import get_db
from .. import models,schemas

router = APIRouter(prefix='/notes', tags=['notes'])

@router.get('',response_model=list[schemas.WorkNoteRead])
def list_notes(task_id: int = Query(..., description="このタスクのノート一覧"), db: Session = Depends(get_db)):
    
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    
    return task.notes

@router.post('', response_model=schemas.WorkNoteRead, status_code=201)
def create_note(payload: schemas.WorkNoteCreate, db: Session = Depends(get_db)):
    
    if db.get(models.Task,payload.task_id) is None:
        raise HTTPException(status_code=400, detail='Task not found')
    
    note = models.WorkNote(**payload.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@router.delete('/{note_id}', status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.get(models.WorkNote, note_id)
    
    if not note:
        raise HTTPException(status_code=404, detail='Note not found')
    
    db.delete(note)
    db.commit()
    return Response(status_code=204)