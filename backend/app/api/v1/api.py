from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.classrooms import router as classrooms_router
from app.api.v1.endpoints.cameras import router as cameras_router
from app.api.v1.endpoints.monitoring_sessions import (
    router as monitoring_sessions_router,
)
from app.api.v1.endpoints.detection_events import (
    router as detection_events_router,
)
from app.api.v1.endpoints.alerts import (
    router as alerts_router,
)
from app.api.v1.endpoints.reports import router as reports_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(classrooms_router)
api_router.include_router(cameras_router)
api_router.include_router(monitoring_sessions_router)
api_router.include_router(detection_events_router)
api_router.include_router(alerts_router)
api_router.include_router(reports_router)