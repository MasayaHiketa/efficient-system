from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.tasks.router import get_current_user
from sqlalchemy import text

router = APIRouter()


# --------------------------
# ① 月間 KPI
# --------------------------

@router.get("/monthly")
def monthly_kpi(
    year: int = None,
    month: int = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if year is None or month is None:
        # 今月 default
        now = datetime.now()
        year = now.year
        month = now.month

    sql = text("""
        SELECT status, COUNT(*) 
        FROM tasks
        WHERE EXTRACT(YEAR FROM created_at) = :year
          AND EXTRACT(MONTH FROM created_at) = :month
        GROUP BY status
    """)

    result = db.execute(sql, {"year": year, "month": month}).fetchall()

    return [{"status": r[0], "count": r[1]} for r in result]

# --------------------------
# ② 担当者別 KPI
# --------------------------
# @router.get("/by-user")
# def kpi_by_user(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
#     sql = text("""
#         SELECT assignee_id, COUNT(*)
#         FROM tasks
#         GROUP BY assignee_id
#     """)
#     rows = db.execute(sql).fetchall()
#     return [{"user": r[0], "count": r[1]} for r in rows]
@router.get("/by-user")
def kpi_by_user(
    year: int | None = None,
    month: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # デフォルト：今月
    if year is None or month is None:
        today = datetime.now()
        year = year or today.year
        month = month or today.month

    sql = text("""
        SELECT assignee_id, COUNT(*)
        FROM tasks
        WHERE EXTRACT(YEAR FROM created_at) = :year
          AND EXTRACT(MONTH FROM created_at) = :month
        GROUP BY assignee_id
    """)

    rows = db.execute(sql, {"year": year, "month": month}).fetchall()

    return {
        "year": year,
        "month": month,
        "data": [
            {"user": r[0], "count": r[1]}
            for r in rows
        ]
    }


# --------------------------
# 月次タスク数
# --------------------------
@router.get("/monthly-trend")
def monthly_trend_kpi(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    sql = text("""
        SELECT
            DATE_TRUNC('month', created_at) AS month,
            COUNT(*) AS count
        FROM tasks
        GROUP BY month
        ORDER BY month
    """)

    rows = db.execute(sql).fetchall()

    return [
        {
            "month": r[0].strftime("%Y-%m"),
            "count": r[1]
        }
        for r in rows
    ]

# --------------------------
# 完了率
# --------------------------

@router.get("/completion-rate")
def completion_rate(
    year: int | None = None,
    month: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # デフォルト：今月
    if year is None or month is None:
        today = datetime.now()
        year = year or today.year
        month = month or today.month

    params = {"year": year, "month": month}

    # ---------------------------
    # ① 全件数
    # ---------------------------
    sql_total = text("""
        SELECT COUNT(*)
        FROM tasks
        WHERE EXTRACT(YEAR FROM created_at) = :year
          AND EXTRACT(MONTH FROM created_at) = :month
    """)

    # ---------------------------
    # ② 完了（done）件数
    # ---------------------------
    sql_done = text("""
        SELECT COUNT(*)
        FROM tasks
        WHERE status = 'done'
          AND EXTRACT(YEAR FROM created_at) = :year
          AND EXTRACT(MONTH FROM created_at) = :month
    """)

    total = db.execute(sql_total, params).scalar()
    done = db.execute(sql_done, params).scalar()

    rate = done / total if total else 0

    # ---------------------------
    # ③ ステータス別 breakdown
    # ---------------------------
    sql_status = text("""
        SELECT status, COUNT(*)
        FROM tasks
        WHERE EXTRACT(YEAR FROM created_at) = :year
          AND EXTRACT(MONTH FROM created_at) = :month
        GROUP BY status
    """)

    rows = db.execute(sql_status, params).fetchall()

    # dict 化
    status_counts = {"todo": 0, "in_progress": 0, "done": 0}
    for s, c in rows:
        status_counts[s] = c

    return {
        "year": year,
        "month": month,
        "completion_rate": rate,
        "done": done,
        "total": total,
        "status_counts": status_counts,
    }

# @router.get("/completion-rate")
# def completion_rate(
#     year: int | None = None,
#     month: int | None = None,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user)
# ):
#     # デフォルト：今月
#     if year is None or month is None:
#         today = datetime.now()
#         year = year or today.year
#         month = month or today.month

#     sql_total = text("""
#         SELECT COUNT(*)
#         FROM tasks
#         WHERE EXTRACT(YEAR FROM created_at) = :year
#           AND EXTRACT(MONTH FROM created_at) = :month
#     """)

#     sql_done = text("""
#         SELECT COUNT(*)
#         FROM tasks
#         WHERE status = 'done'
#           AND EXTRACT(YEAR FROM created_at) = :year
#           AND EXTRACT(MONTH FROM created_at) = :month
#     """)

#     total = db.execute(sql_total, {"year": year, "month": month}).scalar()
#     done = db.execute(sql_done, {"year": year, "month": month}).scalar()

#     rate = done / total if total else 0

#     return {
#         "year": year,
#         "month": month,
#         "completion_rate": rate,
#         "done": done,
#         "total": total,
#     }
