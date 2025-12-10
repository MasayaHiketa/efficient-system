---
---

## ✅ **Efficient System – Backend API (FastAPI + PostgreSQL + Docker)**

**Production-ready backend for task management, activity logs, and KPI analytics**

```md
# Efficient System – Backend API (FastAPI + PostgreSQL + Docker)

Efficient System is a backend service for task management, activity logging, and KPI analytics.  
It is designed for production use, running fully on Docker with FastAPI, PostgreSQL, and Nginx
(proxy handled by the frontend project).

This repository provides:
- Task CRUD API  
- Automatic activity logging  
- KPI analytics (monthly, completion rate, by user)  
- JWT authentication  
- Docker-based deployment  

---

## ✅ System Architecture

```

Frontend (Vue3)
│  Axios /api/
▼
Nginx (Reverse Proxy)
│
▼
FastAPI (efficient-system)
│
▼
PostgreSQL (Task, User, Log tables)

```

---

## ✅ ERD – Entity Relationship Diagram

```

+----------------------+
|       users          |
+----------------------+
| id (PK)              |
| username             |
| email                |
| hashed_password      |
| created_at           |
+----------+-----------+
|
| 1 - N
|
+----------v-----------+
|       tasks          |
+----------------------+
| id (PK)              |
| title                |
| description          |
| status               |
| due_date             |
| assignee_id (FK→users.id)
| created_at           |
| updated_at           |
+----------+-----------+
|
| 1 - N
|
+----------v-----------+
|     activity_logs    |
+----------------------+
| id (PK)              |
| user_id (FK→users.id)|
| task_id (FK→tasks.id)|
| action_type          |
| detail               |
| created_at           |
+----------------------+

````

---

## ✅ Technologies

| Component | Technology |
|----------|------------|
| API Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Auth | JWT (PyJWT) |
| Reverse Proxy (external) | Nginx |
| Containerization | Docker / Docker Compose |

---



# ✅ **API Specification Overview**

## ✅ Authentication

### **POST /auth/register**

Request:

```json
{
  "username": "user1",
  "email": "user1@example.com",
  "password": "test123"
}
```

### **POST /auth/login**

Response:

```json
{
  "access_token": "xxxxx.yyyyy.zzzzz",
  "token_type": "bearer"
}
```

---

## ✅ **Tasks**

### **GET /tasks/?year=2025&month=12**

Returns tasks for the specified month.

### **POST /tasks/**

```json
{
  "title": "New Task",
  "description": "Details",
  "status": "todo",
  "assignee_id": 1,
  "due_date": "2025-12-05T10:00:00"
}
```

### **GET /tasks/{id}**

### **PUT /tasks/{id}**

### **DELETE /tasks/{id}**

---

## ✅ **Activity Logs**

### **GET /logs/?year=2025&month=12**

### **GET /logs/?task_id=10**

Log example:

```json
{
  "id": 1,
  "task_id": 5,
  "user_id": 1,
  "action_type": "task_updated",
  "detail": "Status changed to in_progress",
  "created_at": "2025-12-07T07:20:16Z"
}
```

---

## ✅ **KPI Analytics**

### **GET /kpi/by-user?year=2025&month=12**

Returns task count grouped by assignee.

### **GET /kpi/monthly?year=2025&month=12**

Returns month-level summary.

### **GET /kpi/completion-rate?year=2025&month=12**

Returns:

```json
{
  "total_tasks": 20,
  "completed_tasks": 12,
  "completion_rate": 0.60
}
```

---

# ✅ Project Structure

```
efficient-system/
│
├── app/
│   ├── main.py
│   ├── db.py
│   ├── dependencies.py
│   ├── models.py
│   ├── schemas.py
│   │
│   ├── auth/        # JWT login/register
│   ├── tasks/       # CRUD
│   ├── logs/        # Activity logs
│   └── kpi/         # KPI analytics
│
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## ✅ Environment Variables

`.env` example:

```
DATABASE_URL=postgresql://postgres:Pg18@2025@db:5432/efficient_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

---

## ✅ Deployment Notes

* API is `/api/` when accessed through Nginx
* Direct FastAPI route is /

---


