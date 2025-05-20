#main.py
from fastapi import FastAPI, APIRouter
from fastapi.concurrency import asynccontextmanager
from app.core.config import settings
from app.core.database import create_db_and_tables, engine
from app.routes.course_routes import course_router  # Import the router from routes.py
from app.routes.enrollment_routes import enrollment_router  # Import the router from routes.py
from app.routes.student_routes import student_router  # Import the router from routes.py
from app.routes.role_routes import role_router  # Import the router from routes.py
from app.routes.user_routes import user_router  # Import the router from routes.py
# from app.routes.auth_routes import auth_router  # Import the router from routes.py



router = APIRouter()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up: Creating database tables...")
    create_db_and_tables()
    yield
    print("Shutting down: Cleaning up resources...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)
# Register course_router
app.include_router(course_router, prefix="/courses", tags=["Courses"])
# Register enrollment_router
app.include_router(enrollment_router, prefix="/enrollments", tags=["Enrollments"])
# Register student_router
app.include_router(student_router, prefix="/students", tags=["Students"])
# Register role_router
app.include_router(role_router, prefix="/roles", tags=["Roles"])
# Register user_router
app.include_router(user_router, prefix="/users", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Hub Institute API"}
#create endpoint for health check database connection
@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            return {"status": "Database connection is healthy"}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}
