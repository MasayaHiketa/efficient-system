# app/tasks/seed.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
from app.db import get_db
from app.models import Task,User
from app.tasks.router import get_current_user
from app.models import Task, ActivityLog
router = APIRouter()

# ===============================
# 2023〜2025 の均等分布でタスク生成
# ===============================
@router.post("/seed/{count}")
def seed_tasks(
    count: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    ダッシュボード用の大量タスク生成
    - 2023〜2025 に均等分布
    - 今月：done ≈ 40%
    - 過去：done ≈ 90%
    - due_date は created_at 以降 1〜40日
    - ActivityLog も同時生成
    """

    now = datetime.now()
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 12, 31)
    total_seconds = int((end_date - start_date).total_seconds())

    # 全ユーザー取得
    valid_users = db.query(User.id).all()
    valid_users = [u[0] for u in valid_users]

    for i in range(count):

        # --------------------------
        # ランダム created_at
        # --------------------------
        rand_sec = random.randint(0, total_seconds)
        created_at = start_date + timedelta(seconds=rand_sec)

        # --------------------------
        # 月別の status 重みを変更
        # --------------------------
        if created_at.year == now.year and created_at.month == now.month:
            # 今月：done ≈ 30〜40%
            statuses = ["todo", "in_progress", "done"]
            weights = [0.4, 0.3, 0.3]
        else:
            # 過去：ほぼ done
            statuses = ["todo", "in_progress", "done"]
            weights = [0.05, 0.05, 0.90]

        status = random.choices(statuses, weights=weights, k=1)[0]

        # due_date
        due_date = created_at + timedelta(days=random.randint(1, 40))

        # --------------------------
        # Task 作成
        # --------------------------
        t = Task(
            title=f"Seed Task {i}",
            description="Auto-generated",
            status=status,
            assignee_id=random.choice(valid_users),
            creator_id=current_user.id,
            created_at=created_at,
            updated_at=created_at,
            due_date=due_date,
        )

        db.add(t)
        db.flush()  # task.id を取得するため

        # --------------------------
        # Activity Log 生成
        # --------------------------
        log = ActivityLog(
            task_id=t.id,
            user_id=current_user.id,
            action_type="task_created",
            detail="Seeded task",
            created_at=created_at
        )
        db.add(log)

    db.commit()

    return {"message": f"{count} tasks created with logs!"}

# @router.post("/seed/{count}")
# def seed_tasks(
#     count: int,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user),
# ):
#     """
#     ダッシュボード用の大量タスク生成
#     - 2023〜2025 に均等分布
#     - status 比率調整
#     - due_date も created_at 以降に設定
#     """
#     now = datetime.now()
#     statuses = ["todo", "in_progress", "done"]
#     if created_at.year == now.year and created_at.month == now.month:
#         status_weights = [0.4, 0.3, 0.3]   # todo, in_progress, done
#     else:
#         status_weights = [0.05, 0.05, 0.90]  # 過去はほぼ done


#     # 4 年間の範囲
#     start_date = datetime(2023, 1, 1)
#     end_date = datetime(2025, 12, 31)
#     total_seconds = int((end_date - start_date).total_seconds())

#     valid_users = db.query(User.id).all()
#     valid_users = [u[0] for u in valid_users]  # id のリスト化


#     for i in range(count):
#         # --- created_at を完全ランダムに均等生成 ---
#         rand_sec = random.randint(0, total_seconds)
#         created_at = start_date + timedelta(seconds=rand_sec)

#         # --- due_date は created_at 以降 1〜40日 ---
#         due_date = created_at + timedelta(days=random.randint(1, 40))

#         status = random.choices(statuses, weights=status_weights, k=1)[0]

#         t = Task(
#             title=f"Seed Task {i}",
#             description="Auto-generated",
#             status=status,
#             assignee_id=random.choice(valid_users),
#             creator_id=4,
#             created_at=created_at,
#             updated_at=created_at,
#             due_date=due_date,
#         )

#         db.add(t)

#     db.commit()
#     return {"message": f"{count} tasks created!"}
