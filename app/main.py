from contextlib import asynccontextmanager
import asyncio
#from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes_schedules import router as schedules_router
from .services.scheduler import process_due_schedules


background_task: asyncio.Task | None = None
async def scheduler_loop():
    """
    Simple scheduler loop:
    - runs forever
    - every 30 seconds: calls process_due_schedules()
    """
    while True:
        await process_due_schedules()
        await asyncio.sleep(30)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global background_task
    # 🚀 Startup: start background scheduler loop
    background_task = asyncio.create_task(scheduler_loop())
    print("Background scheduler started ✅")

    try:
        yield
    finally:
        # 🛑 Shutdown: cancel loop
        if background_task:
            background_task.cancel()
            try:
                await background_task
            except asyncio.CancelledError:
                pass
        print("Background scheduler stopped ")

app = FastAPI(
    title="Email Scheduler with Public APIs",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(schedules_router, prefix="/schedules", tags=["schedules"])
