from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy import Boolean
from sqlalchemy import Enum as SqlEnum
from app.db.session import Base
import enum


class ProjectStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    ON_HOLD = "ON_HOLD"
    ARCHIVED = "ARCHIVED"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SqlEnum(ProjectStatus), nullable=False, default=ProjectStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
