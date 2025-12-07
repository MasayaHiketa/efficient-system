from sqlalchemy.orm import Session
from app.models import Task, ActivityLog
from datetime import datetime

def create_log(db, user_id, task_id, action, detail=""):
    log = ActivityLog(
        user_id=user_id,
        task_id=task_id,
        action_type=action,
        detail=detail
    )
    db.add(log)
    db.commit()


def create_task(db: Session, user_id: int, data):
    task = Task(
        title=data.title,
        description=data.description,
        assignee_id=data.assignee_id,
        creator_id=user_id,
        status=data.status,
        due_date=data.due_date,
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    create_log(db, user_id, task.id, "task_created", task.title)
    return task


def update_task(db: Session, user_id: int, task: Task, data):
    for key, value in data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    task.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(task)

    create_log(db, user_id, task.id, "task_updated", task.title)
    return task

def delete_task(db: Session, user_id: int, task: Task):
    create_log(db, user_id, task.id, "task_deleted", task.title)
    
    db.delete(task)
    db.commit()

