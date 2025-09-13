Set up the database and connetion.

This project should use:
* Database: SQLite
* DB package: SQLAlchemy
* Migrations: Alembic
* A models.py file to contain the models
* Pydantic classes wherever possible

Lets start with a model for Task planning, it should have models like this:

```
Project
   id: UUID
   name: str


Category
   id: UUID
   name: str

Task
   id: UUID
   description: str
   priority: int
   category: Category
   project: Project
```

Please create the database connection files, the models and an initial migration.