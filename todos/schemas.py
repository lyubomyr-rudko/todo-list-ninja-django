from ninja import ModelSchema
from pydantic import BaseModel
from typing import Optional
from .models import Task


class TaskIn(ModelSchema):
    class Config:
        model = Task
        model_exclude = ["id", "user", "complete", "created"]


class TaskOut(ModelSchema):
    class Config:
        model = Task
        model_fields = ["id", "title", "description", "complete", "created"]


class PartialTaskIn(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    complete: Optional[bool] = None
    class Config:
        orm_mode = True
