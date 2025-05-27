from typing import Annotated
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, Relationship, create_engine, select, UniqueConstraint
import uuid
import requests

# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-models


class MatchPreference(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("project_id", "user_id", name="project_user_unique"),
    )
    id: int | None = Field(default=None, primary_key=True)
    created_at: str = Field(default=datetime.utcnow(), nullable=False)
    user_id: int = Field(foreign_key="user.id")
    project_id: int = Field(foreign_key="project.id")
    matched: int = Field(default=0)

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=False)
    email: str = Field(index=True, unique=True)
    projects: list["Project"] = Relationship(back_populates="owner")
    matches: list["Project"] = Relationship(back_populates="matches", link_model=MatchPreference)

class ProjectTag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    # project: Project | None = Relationship(back_populates="projects")
    tag: str = Field(foreign_key="tag.label")

class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str = Field()
    owner_id: int = Field(foreign_key="user.id")
    owner: User | None = Relationship(back_populates="projects")
    matches: list[User] = Relationship(back_populates="matches", link_model=MatchPreference)

    expires_on: str = Field(default=datetime.utcnow() + timedelta(days=14) , nullable=False)
    created_at: str = Field(default=datetime.utcnow(), nullable=False)
    # tags: list["Tag"] = Relationship(back_populates="tag", link_model=ProjectTag)

class Tag(SQLModel, table=True):
    label: str = Field(index=True, primary_key=True)
    # projects: list[Project] = Relationship(back_populates="project", link_model=ProjectTag)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()
# drop_db_and_tables()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Hello from pairing-tinder!"}

# USER ENDPOINTS
@app.get("/users/{user_id}")
def read_user(user: User, session: SessionDep) -> User:
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    projects = user.projects
    return {
      user: {
        id: user.id,
        name: user.name,
        email: user.email,
        projects: projects      }
    }

# https://fastapi.tiangolo.com/features/?h=auth#security-and-authentication
@app.post("/users/")
def create_user(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
    # session.refresh(user)

#def create_user_from_rc(token, SessionDep) -> User:
#   headers = {'Authorization:': 'Bearer ' + token}
#   rcjson = requests.get('https://www.recurse.com/api/v1/people/me', headers)
#           user = User(
#           rc_id=rcjson.
#           name=rcjson.first_name,
#           email=rcjson.email,
#           github=rcjson.github,
#           batch_id=rcjson.batch.id,
#           batch_name=rcjson.batch.name,
#           start_date=rcjson.batch.start_date,
#           end_date=rcjson.batch.end_date,
#         )
#         session.add(user)
#         session.commit()
#         session.refresh(user)
#   return user
#

# PROJECT ENDPOINTS

@app.post("/projects/")
def create_project(project: Project, session: SessionDep) -> Project:
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@app.get("/projects/")
def read_projects(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Project]:
    # TODO: Filter to un-match-preffed for user
    projects = session.exec(select(Project).offset(offset).limit(limit)).all()
    return projects


@app.get("/projects/{project_id}")
def read_project(project_id: int, session: SessionDep) -> Project:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.delete("/projects/{project_id}")
def delete_project(project_id: int, session: SessionDep):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project)
    session.commit()
    return {"ok": True}

@app.post("/match/")
def match(match: MatchPreference, session: SessionDep) -> MatchPreference:
    session.add(match)
    session.commit()
    session.refresh(match)
    return match