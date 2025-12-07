from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.tasks.router import router as tasks_router
from app.logs.router import router as logs_router
from app.kpi.router import router as kpi_router   
from app.tasks.seed import router as seed_router
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Efficient System API",
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
app.include_router(logs_router, prefix="/logs", tags=["Activity Logs"])
app.include_router(kpi_router, prefix="/kpi", tags=["KPI"])   
app.include_router(seed_router, prefix="/tasks", tags=["Seed"])

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
