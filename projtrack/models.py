from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.dialects.sqlite import CHAR
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.orm import relationship
import uuid
from .database import Base

class UUID(TypeDecorator):
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID())
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value)
            return value

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(UUID(), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    
    tasks = relationship("Task", back_populates="project")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(UUID(), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    
    tasks = relationship("Task", back_populates="category")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(UUID(), primary_key=True, default=uuid.uuid4, index=True)
    description = Column(String, nullable=False)
    priority = Column(Integer, nullable=False)
    category_id = Column(UUID(), ForeignKey("categories.id"))
    project_id = Column(UUID(), ForeignKey("projects.id"))
    
    category = relationship("Category", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")