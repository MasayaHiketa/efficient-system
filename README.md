```md
# Efficient System – Backend API (FastAPI + PostgreSQL)

This repository contains the backend API for **Efficient System**, a task and activity log management platform.  
The backend is built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy**, featuring JWT authentication, activity logs, KPI analytics, and full Docker support.

---

## 🚀 Features

- **User Authentication**  
  - JWT-based login  
  - Role-based access control (admin/user)

- **Task Management**  
  - Create / Update / Delete / List tasks  
  - Monthly filtering (year/month query parameters)  
  - Auto-generated activity logs on every update

- **Activity Logs**  
  - Track task creation, updates, deletions  
  - Filter by month or task_id

- **KPI Endpoints**  
  - Monthly trend  
  - Completion rate  
  - Task distribution by assignee

- **Full Docker Support**  
  - API, PostgreSQL, Nginx (proxy)  
  - Production-ready configuration

---

## 🏗️ Project Structure

```

efficient-system/
│
├── app/
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth/
│   ├── tasks/
│   └── logs/
│
├── Dockerfile
└── requirements.txt

```

---

## 🔧 Environment Variables

Create a `.env` file:

```

DATABASE_URL=postgresql://postgres:password@db:5432/efficient_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256

````

---

## ▶️ Run Locally

### Install dependencies
```bash
pip install -r requirements.txt
````

### Start API

```bash
uvicorn app.main:app --reload
```

### Open API Docs

[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🐳 Run with Docker

### Build & Compose

```bash
docker compose up --build
```

This will start:

* FastAPI backend
* PostgreSQL
* Nginx reverse proxy

---

## 📌 API Examples

### Login

```http
POST /auth/login
{
  "username": "user1",
  "password": "test123"
}
```

### List tasks

```http
GET /tasks?year=2025&month=12
Authorization: Bearer <token>
```

### Create task

```http
POST /tasks/
```

---
