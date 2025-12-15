from pydantic import BaseModel, Field
from pydantic import ConfigDict
from typing import Optional
from datetime import datetime
from app.models.project import ProjectStatus
from typing import List
from pydantic import ConfigDict


class ProjectCreate(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    status: Optional[ProjectStatus] = ProjectStatus.ACTIVE


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[ProjectStatus]


class StatusUpdate(BaseModel):
    status: ProjectStatus


class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: ProjectStatus
    created_at: datetime
    finished_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class Paging(BaseModel):
    limit: int
    offset: int
    total: int


class ProjectResponse(BaseModel):
    data: ProjectOut
    model_config = ConfigDict(from_attributes=True)


class ProjectListResponse(BaseModel):
    data: List[ProjectOut]
    paging: Paging
    model_config = ConfigDict(from_attributes=True)
