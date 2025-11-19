from pathlib import Path

from dotenv import load_dotenv

from challenges.c03_sql_failures.sqlUtils.databaseDAO import (
    initialize_database_if_needed,
    run_applicant_query,
    test_connection,
)
from common.logging_config import get_logger

load_dotenv()
logger = get_logger(__name__)

# --- CONSTANTS ---
BASE_DIR = Path(__file__).resolve().parent
QUERY_SQL = BASE_DIR / "applicant_query.sql"


def main() -> None:
    logger.info("[CH03] Starting Challenge 3 execution...")

    # Test DB connection
    if not test_connection():
        logger.error("[CH03] Database connection failed. Aborting.")
        return

    # Ensure DB is initialized
    initialize_database_if_needed()

    logger.info(f"[CH03] Executing query: {QUERY_SQL.name}")
    rows = run_applicant_query(str(QUERY_SQL))

    logger.info("[CH03] ===============================")
    logger.info("[CH03] Query Results:")
    for row in rows:
        logger.info(dict(row))
    logger.info("[CH03] ===============================")

    logger.info("[CH03] Challenge 3 execution complete.")


if __name__ == "__main__":
    main()
