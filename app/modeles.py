from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class TaskGroup(Base):
    __tablename__ = 'task_groups'
    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    tasks: Mapped[list['Task']] = relationship(
        back_populates='group',
        cascade="all, delete-orphan"
    )
    

class Task(Base):
    __tablename__ = 'tasks'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default='todo')
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    group_id: Mapped[int | None] = mapped_column(ForeignKey('task_groups.id'),nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    group: Mapped[TaskGroup | None] = relationship(back_populates='tasks')