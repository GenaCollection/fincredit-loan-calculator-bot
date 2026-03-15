"""Database connection and session management"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import config
from database.models import Base

engine = None
Session = None

def init_db():
    """Initialize database and create all tables"""
    global engine, Session
    
    engine = create_engine(config.DATABASE_URL, echo=False)
    Session = scoped_session(sessionmaker(bind=engine))
    
    # Create all tables
    Base.metadata.create_all(engine)
    def get_session():
        """Get database session"""
    if Session is None:
        init_db()
    return Session()
