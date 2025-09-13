from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.orm import relationship, Mapped
import uuid
from .database import Base


class UUID(TypeDecorator):
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID())
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
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

    id: Mapped[uuid.UUID] = Column(
        UUID(), primary_key=True, default=uuid.uuid4, index=True
    )
    name: Mapped[str] = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="project")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = Column(
        UUID(), primary_key=True, default=uuid.uuid4, index=True
    )
    name: Mapped[str] = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="category")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = Column(
        UUID(), primary_key=True, default=uuid.uuid4, index=True
    )
    description: Mapped[str] = Column(String, nullable=False)
    priority: Mapped[int] = Column(Integer, nullable=False)
    category_id: Mapped[uuid.UUID | None] = Column(UUID(), ForeignKey("categories.id"))
    project_id: Mapped[uuid.UUID | None] = Column(UUID(), ForeignKey("projects.id"))

    category = relationship("Category", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")
