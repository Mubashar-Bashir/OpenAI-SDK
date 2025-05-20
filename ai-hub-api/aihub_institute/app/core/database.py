#database.py
from sqlmodel import create_engine, Session, SQLModel
from ..core.config import settings

#tables creation from schema
from ..models.user import User  # Import all models needed for table creation


# Create engine for async SQLAlchemy operations
engine = create_engine(
    settings.SYNC_DATABASE_URL,
    echo=True,
    connect_args={"sslmode": "require"},  # Required for Neon PostgreSQL
)

def get_session():
    with Session(engine) as session:
        yield session
        
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)  # This creates all tables based on models
