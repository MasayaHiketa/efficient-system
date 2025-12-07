from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import ActivityLog
from app.schemas import ActivityLogOut
from app.tasks.router import get_current_user
from sqlalchemy import extract
router = APIRouter()

@router.get("/")
def get_logs(
    task_id: int | None = None,
    year: int | None = None,
    month: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    query = db.query(ActivityLog)

    # -------------------------
    # ① 特定タスクのログ取得
    # -------------------------
    if task_id is not None:
        query = query.filter(ActivityLog.task_id == task_id)

    else:
        # -------------------------
        # ② 月次ログ（year + month）
        # -------------------------
        now = datetime.now()

        if year is None:
            year = now.year

        if month is None:
            month = now.month

        query = query.filter(
            extract("year", ActivityLog.created_at) == year,
            extract("month", ActivityLog.created_at) == month
        )

    logs = query.order_by(ActivityLog.created_at.desc()).all()

    return [
        {
            "id": log.id,
            "task_id": log.task_id,
            "user_id": log.user_id,
            "action_type": log.action_type,
            "detail": log.detail,
            "created_at": log.created_at,
        }
        for log in logs
    ]

# @router.get("/")
# def get_logs(
#     task_id: int | None = None,
#     days: int = 7,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user)
# ):
#     query = db.query(ActivityLog)

#     if task_id:
#         query = query.filter(ActivityLog.task_id == task_id)

#     else:
#         since = datetime.now() - timedelta(days=days)
#         query = query.filter(ActivityLog.created_at >= since)

#     query = query.order_by(ActivityLog.created_at.desc())

#     logs = query.all()

#     return [
#         {
#             "id": log.id,
#             "task_id": log.task_id,
#             "user_id": log.user_id,
#             "action_type": log.action_type,
#             "detail": log.detail,
#             "created_at": log.created_at,
#         }
#         for log in logs
#     ]


@router.get("/by-task/{task_id}")
def logs_by_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    logs = db.query(ActivityLog).filter(
        ActivityLog.task_id == task_id
    ).order_by(ActivityLog.created_at.desc()).all()

    return logs
