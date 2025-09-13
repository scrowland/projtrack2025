from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional

class ProjectBase(BaseModel):
    name: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: UUID
    
    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: UUID
    
    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    description: str
    priority: int

class TaskCreate(TaskBase):
    category_id: UUID
    project_id: UUID

class Task(TaskBase):
    id: UUID
    category_id: UUID
    project_id: UUID
    category: Optional[Category] = None
    project: Optional[Project] = None
    
    class Config:
        from_attributes = True