"""
Database connection, session management, and schema initialization.
Uses SQLAlchemy with PyMySQL driver for MySQL.
"""

import os
from contextlib import contextmanager
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base

# Load environment variables from .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "codebase_evolution")

# Format database URLs
def get_server_url() -> str:
    """Returns database URL without database name, used to create the DB if missing."""
    return f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?charset=utf8mb4"

def get_database_url() -> str:
    """Returns full database connection URL."""
    return f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

def create_database_if_not_exists():
    """Connects to MySQL server and creates the target database if it does not already exist."""
    server_url = get_server_url()
    temp_engine = create_engine(server_url, isolation_level="AUTOCOMMIT")
    with temp_engine.connect() as conn:
        conn.execute(
            text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        )
    temp_engine.dispose()

# Global engine and sessionmaker
_engine = None
_SessionFactory = None

def get_engine():
    """Initializes and returns the singleton SQLAlchemy engine."""
    global _engine
    if _engine is None:
        create_database_if_not_exists()
        _engine = create_engine(
            get_database_url(),
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=10,
            max_overflow=20,
            echo=False
        )
    return _engine

def get_session():
    """Returns a new SQLAlchemy session."""
    global _SessionFactory
    if _SessionFactory is None:
        engine = get_engine()
        _SessionFactory = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    return _SessionFactory()

@contextmanager
def get_db_context():
    """Context manager for handling sessions with automatic commit/rollback."""
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def init_db():
    """Ensures database exists and creates all required tables."""
    create_database_if_not_exists()
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

def test_connection():
    """
    Tests MySQL connection.
    Returns (True, "Connected successfully") or (False, error_message).
    """
    try:
        create_database_if_not_exists()
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            if result == 1:
                return True, f"Successfully connected to MySQL database '{DB_NAME}' on {DB_HOST}:{DB_PORT}"
            return False, "Unexpected result from database query"
    except Exception as e:
        return False, f"MySQL connection failed: {str(e)}"
