from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class TaskGroup(Base):
    __tablename__ = 'task_groups'
    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)