from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ---------------------
# User
# ---------------------

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        orm_mode = True


# ---------------------
# Auth
# ---------------------
class LoginRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# ---------------------
# Task
# ---------------------

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "todo"
    assignee_id: Optional[int] = None
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskOut(TaskBase):
    id: int
    creator_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ---------------------
# Activity Log
# ---------------------

class ActivityLogOut(BaseModel):
    id: int
    user_id: int
    task_id: Optional[int]
    action_type: str
    detail: str
    created_at: datetime

    class Config:
        orm_mode = True
