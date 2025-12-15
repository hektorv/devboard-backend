from pydantic import BaseModel, Field
from pydantic import ConfigDict
from typing import Optional
from datetime import datetime
from app.models.task import TaskStatus, TaskPriority
from typing import List
from pydantic import ConfigDict


class TaskCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.BACKLOG
    priority: Optional[TaskPriority] = TaskPriority.MEDIUM
    assignee_user_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus]
    priority: Optional[TaskPriority]
    assignee_user_id: Optional[int]


class TaskOut(BaseModel):
    id: int
    project_id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    assignee_user_id: Optional[int]
    created_at: datetime
    finished_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class TaskResponse(BaseModel):
    data: TaskOut
    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    data: List[TaskOut]
    paging: dict
    model_config = ConfigDict(from_attributes=True)
