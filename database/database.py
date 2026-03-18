"""Database connection and session management"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import text
import config
from database.models import Base

engine = None
Session = None

def _maybe_migrate_sqlite_schema(engine):
    """
    Lightweight migration for existing SQLite DBs created with old column names.
    We don't use Alembic in this project, so we patch schema in-place.
    """
    if not str(engine.url).startswith("sqlite"):
        return

    with engine.begin() as conn:
        # loans table: old schema used amount/interest_rate/term_months/overpayment
        loans_cols = [row[1] for row in conn.execute(text("PRAGMA table_info(loans)")).fetchall()]
        if loans_cols:
            rename_map = {
                "amount": "principal",
                "interest_rate": "annual_rate",
                "term_months": "months",
                "overpayment": "total_overpayment",
            }

            for old, new in rename_map.items():
                if old in loans_cols and new not in loans_cols:
                    conn.execute(text(f"ALTER TABLE loans RENAME COLUMN {old} TO {new}"))

            # refresh after renames
            loans_cols = [row[1] for row in conn.execute(text("PRAGMA table_info(loans)")).fetchall()]

            # Add new columns if missing (safe no-op if they exist)
            add_columns = {
                "first_payment_date": "DATETIME",
                "has_insurance": "BOOLEAN NOT NULL DEFAULT 0",
                "insurance_monthly": "FLOAT NOT NULL DEFAULT 0.0",
                "has_extra_payments": "BOOLEAN NOT NULL DEFAULT 0",
                "extra_payment_amount": "FLOAT NOT NULL DEFAULT 0.0",
                "extra_payment_type": "VARCHAR(20)",
                "reduction_type": "VARCHAR(20)",
                "use_exact_days": "BOOLEAN NOT NULL DEFAULT 1",
                "actual_months": "INTEGER",
            }

            for col, ddl in add_columns.items():
                if col not in loans_cols:
                    conn.execute(text(f"ALTER TABLE loans ADD COLUMN {col} {ddl}"))


def init_db():
    """Initialize database and create all tables"""
    global engine, Session
    
    engine = create_engine(config.DATABASE_URL, echo=False)
    Session = scoped_session(sessionmaker(bind=engine))
    
    # Create all tables
    Base.metadata.create_all(engine)
    _maybe_migrate_sqlite_schema(engine)
    

def get_session():
    """Get database session"""
    if Session is None:
        init_db()
    return Session()
