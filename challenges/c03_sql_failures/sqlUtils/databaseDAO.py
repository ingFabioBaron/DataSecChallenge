import os
import sqlite3
from pathlib import Path
from typing import List, Optional
from common.logging_config import get_logger

logger = get_logger(__name__)

# ============================================================
# DIRECTORY & PATH RESOLUTION
# ============================================================

def _base_dir() -> Path:
    """
    Returns the base directory of challenge 03.
    """
    return Path(__file__).resolve().parent.parent  # .../c03_sql_failures_report/


def _sql_dir() -> Path:
    """
    Returns the path to the sqlUtils directory.
    """
    return _base_dir() / "sqlUtils"


def _schema_sql_path() -> Path:
    return _sql_dir() / "schema.sql"


def _sample_data_sql_path() -> Path:
    return _sql_dir() / "sample_data.sql"


# ============================================================
# DB PATH HANDLING
# ============================================================

def load_db_path() -> Path:
    """
    Loads DB_PATH from .env or uses default
    ./c03_sql_failures_report/database.sqlite3

    Ensures the folder exists.
    """
    db_path = os.getenv("DB_PATH")

    if not db_path:
        logger.warning(
            "[DB] Environment variable DB_PATH not set. "
            "Using default: ./c03_sql_failures_report/database.sqlite3"
        )
        db_path = str(_base_dir() / "database.sqlite3")

    db_file = Path(db_path).resolve()

    # Ensure directory exists
    if not db_file.parent.exists():
        logger.info(f"[DB] Creating directory for database: {db_file.parent}")
        db_file.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"[DB] Using database file: {db_file}")
    return db_file


# ============================================================
# CONNECTION HANDLING
# ============================================================

def connect() -> sqlite3.Connection:
    """
    Creates a SQLite connection using DB_PATH.
    Ensures directory exists.
    """
    db_file = load_db_path()

    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        logger.info("[DB] Connection established successfully.")
        return conn

    except sqlite3.Error as e:
        logger.error(f"[DB] Connection failed: {e}")
        raise


def test_connection() -> bool:
    logger.info("[DB] Testing database connection...")

    try:
        conn = connect()
        conn.execute("SELECT 1;")
        conn.close()

        logger.info("[DB] Connection test OK.")
        return True

    except sqlite3.Error as e:
        logger.error(f"[DB] Connection test FAILED: {e}")
        return False


# ============================================================
# SQL EXECUTION UTILITIES
# ============================================================

def _run_sql_file(conn: sqlite3.Connection, sql_path: Path) -> None:
    """
    Executes all SQL statements inside a .sql file.
    """
    if not sql_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_path}")

    logger.info(f"[DB] Executing SQL file: {sql_path.name}")

    with sql_path.open("r", encoding="utf-8") as f:
        script = f.read()

    try:
        conn.executescript(script)
        conn.commit()
        logger.info(f"[DB] SQL script executed OK: {sql_path.name}")

    except sqlite3.Error as e:
        logger.error(f"[DB] SQL execution error in {sql_path.name}: {e}")
        raise


# ============================================================
# SCHEMA + DATA LOADING
# ============================================================

def initialize_database_if_needed() -> None:
    """
    Creates & populates database ONLY IF tables do not exist.
    """
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='customers';
    """)

    exists = cursor.fetchone()

    if exists:
        logger.info("[DB] Database already initialized. Skipping schema creation.")
        conn.close()
        return

    logger.info("[DB] Initializing database from scratch...")

    # Create schema
    _run_sql_file(conn, _schema_sql_path())

    # Load sample data
    _run_sql_file(conn, _sample_data_sql_path())

    conn.close()
    logger.info("[DB] Database initialization complete.")


# ============================================================
# QUERY EXECUTION
# ============================================================

def execute_query(query: str, params: Optional[List] = None) -> List[sqlite3.Row]:
    """
    Executes a SELECT query and returns rows.
    """
    if params is None:
        params = []

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(query, params)
        rows = cur.fetchall()
        logger.info(f"[DB] Query completed, {len(rows)} rows returned.")
        return rows

    except sqlite3.Error as e:
        logger.error(f"[DB] Query error: {e}")
        raise

    finally:
        conn.close()


def run_applicant_query(query_file_path: str) -> List[sqlite3.Row]:
    """
    Loads applicant_query.sql and executes it.
    """
    sql_path = Path(query_file_path)

    if not sql_path.exists():
        raise FileNotFoundError(f"Query file not found: {sql_path}")

    with sql_path.open("r", encoding="utf-8") as f:
        query = f.read()

    return execute_query(query)
