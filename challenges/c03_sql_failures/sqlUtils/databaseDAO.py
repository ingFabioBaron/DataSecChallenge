"""
Database Data Access Object (DAO) for Challenge 03: SQL Failures Report.

Provides:
- Directory and path resolution for SQL files and database.
- SQLite connection handling.
- Schema and sample data initialization.
- SQL query execution utilities.
"""

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
    """
    Returns the path to the schema.sql file.
    """
    return _sql_dir() / "schema.sql"


def _sample_data_sql_path() -> Path:
    """
    Returns the path to the sample_data.sql file.
    """
    return _sql_dir() / "sample_data.sql"


# ============================================================
# DB PATH HANDLING
# ============================================================


def load_db_path() -> Path:
    """
    Loads DB_PATH from environment variable or uses default
    ./c03_sql_failures_report/database.sqlite3.

    Ensures the folder exists.

    Returns:
        Path: Resolved path to the SQLite database file.
    """
    db_path = os.getenv("DB_PATH")

    if not db_path:
        logger.warning(
            "[DB] Environment variable DB_PATH not set. "
            "Using default: ./c03_sql_failures_report/database.sqlite3"
        )
        db_path = str(_base_dir() / "database.sqlite3")

    db_file = Path(db_path).resolve()

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
    Creates a SQLite connection using DB_PATH and ensures directory exists.

    Returns:
        sqlite3.Connection: Active SQLite connection.

    Raises:
        sqlite3.Error: If connection fails.
    """
    db_file = load_db_path()

    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        logger.info("[DB] Connection established successfully.")
        return conn

    except sqlite3.Error as error:
        logger.error(f"[DB] Connection failed: {error}")
        raise


def test_connection() -> bool:
    """
    Tests database connectivity.

    Returns:
        bool: True if connection works, False otherwise.
    """
    logger.info("[DB] Testing database connection...")

    try:
        conn = connect()
        conn.execute("SELECT 1;")
        conn.close()

        logger.info("[DB] Connection test OK.")
        return True

    except sqlite3.Error as error:
        logger.error(f"[DB] Connection test FAILED: {error}")
        return False


# ============================================================
# SQL EXECUTION UTILITIES
# ============================================================


def _run_sql_file(conn: sqlite3.Connection, sql_path: Path) -> None:
    """
    Executes all SQL statements inside a .sql file.

    Args:
        conn (sqlite3.Connection): Active database connection.
        sql_path (Path): Path to SQL file.

    Raises:
        FileNotFoundError: If SQL file does not exist.
        sqlite3.Error: If execution fails.
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

    except sqlite3.Error as error:
        logger.error(f"[DB] SQL execution error in {sql_path.name}: {error}")
        raise


# ============================================================
# SCHEMA + DATA LOADING
# ============================================================


def initialize_database_if_needed() -> None:
    """
    Creates and populates database only if tables do not exist.
    """
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='customers';
        """
    )

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

    Args:
        query (str): SQL query to execute.
        params (Optional[List]): Parameters for the query.

    Returns:
        List[sqlite3.Row]: List of rows returned by the query.

    Raises:
        sqlite3.Error: If query execution fails.
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

    except sqlite3.Error as error:
        logger.error(f"[DB] Query error: {error}")
        raise

    finally:
        conn.close()


def run_applicant_query(query_file_path: str) -> List[sqlite3.Row]:
    """
    Loads a SQL file and executes the query.

    Args:
        query_file_path (str): Path to the SQL file.

    Returns:
        List[sqlite3.Row]: List of rows returned by the query.

    Raises:
        FileNotFoundError: If SQL file does not exist.
        sqlite3.Error: If query execution fails.
    """
    sql_path = Path(query_file_path)

    if not sql_path.exists():
        raise FileNotFoundError(f"Query file not found: {sql_path}")

    with sql_path.open("r", encoding="utf-8") as f:
        query = f.read()

    return execute_query(query)
