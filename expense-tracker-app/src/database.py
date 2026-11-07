import os
from contextlib import contextmanager
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")  # .env is in the project root

_REQUIRED_VARS = ("DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD")


def _settings():
    missing = [name for name in _REQUIRED_VARS if not os.getenv(name)]
    if missing:
        raise RuntimeError(f"Missing .env settings: {', '.join(missing)}")

    return {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }


# terminal and dashboard
def get_connection():
    return psycopg2.connect(**_settings(), connect_timeout=5)

@contextmanager
def db_connection():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# SQLAlchemy: API
_session_factory = None

def get_session_factory():
    global _session_factory

    if _session_factory is None:
        from sqlalchemy import create_engine
        from sqlalchemy.engine import URL
        from sqlalchemy.orm import sessionmaker

        s = _settings()
        url = URL.create(
            "postgresql+psycopg2",
            username=s["user"],
            password=s["password"], 
            host=s["host"],
            port=int(s["port"]),
            database=s["dbname"],
        )
        engine = create_engine(url, pool_pre_ping=True)
        _session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return _session_factory      