from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Task,User
from app.schemas import TaskCreate, TaskUpdate, TaskOut
from app.tasks.service import create_task, update_task,delete_task
from fastapi.security import OAuth2PasswordBearer,HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from sqlalchemy import text
from datetime import datetime, timedelta
from sqlalchemy import extract


router = APIRouter()
now = datetime.now()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = "secret"
ALGORITHM = "HS256"

bearer = HTTPBearer()

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db=Depends(get_db)
):
    token = creds.credentials  

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(401, "Invalid token")
    except JWTError:
        raise HTTPException(401, "Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(401, "User not found")

    return user

# --- CREATE ---
@router.post("/", response_model=TaskOut)
def create_task_route(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_task(db, current_user.id, data)


# --- LIST ---
# @router.get("/", response_model=list[TaskOut])
# def list_tasks(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return db.query(Task).all()
@router.get("/", response_model=list[TaskOut])
def list_tasks(
    year: int | None = None,
    month: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    year/month が指定されない場合は「今月」を返す。
    """
    now = datetime.now()

    # デフォルト：今年・今月
    year = year or now.year
    month = month or now.month

    q = db.query(Task)

    q = q.filter(extract("year", Task.created_at) == year)
    q = q.filter(extract("month", Task.created_at) == month)

    return q.order_by(Task.created_at.desc()).all()



@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")

    return task

# --- UPDATE ---
@router.put("/{task_id}", response_model=TaskOut)
def update_task_route(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(403, "Admin only")
    
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")

    return update_task(db, current_user.id, task, data)


# -----------------------
# 全タスク削除 API
# -----------------------
@router.delete("/reset")
def reset_all(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # 1. logs を先に削除
    db.execute(text("DELETE FROM activity_logs"))

    # 2. tasks を削除
    db.execute(text("DELETE FROM tasks"))

    db.commit()

    return {"message": "All tasks and logs deleted"}

# --- DELETE ---
@router.delete("/{task_id}", status_code=204)
def delete_task_route(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(403, "Admin only")

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")

    delete_task(db, current_user.id, task)
    return {"message": "deleted"}


