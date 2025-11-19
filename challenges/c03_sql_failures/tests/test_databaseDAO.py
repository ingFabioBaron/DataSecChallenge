import sqlite3
import tempfile
from pathlib import Path

import pytest

from challenges.c03_sql_failures.sqlUtils import databaseDAO
from common.logging_config import get_logger

logger = get_logger(__name__)


# ---------------------------
# Fixtures
# ---------------------------

@pytest.fixture
def temp_db_path(monkeypatch):
    """
    Creates a temporary SQLite database file and sets DB_PATH env var.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = Path(tmpdir) / "test_db.sqlite3"
        # Ensure parent exists (TemporaryDirectory exists)
        monkeypatch.setenv("DB_PATH", str(db_file))
        yield db_file
        # tempdir and contents removed automatically


@pytest.fixture
def temp_sql_dir(tmp_path, monkeypatch):
    """
    Creates a temporary sqlUtils folder with schema.sql, sample_data.sql and applicant_query.sql.
    Monkeypatches nothing in the DAO; tests will call the DAO's functions directly passing paths.
    """
    sql_dir = tmp_path / "sqlUtils"
    sql_dir.mkdir(parents=True, exist_ok=True)

    # --- schema.sql (from your corrected schema) ---
    schema_sql = sql_dir / "schema.sql"
    schema_sql.write_text(
        """-- schema.sql
-- Schema for Challenge 3: Advertising System Failures Report

-- ============================
-- Table: customers
-- ============================
CREATE TABLE customers (
    id          INTEGER PRIMARY KEY,
    first_name  TEXT NOT NULL,
    last_name   TEXT NOT NULL
);

-- ============================
-- Table: campaigns
-- ============================
CREATE TABLE campaigns (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    name        TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- ============================
-- Table: events
-- ============================
CREATE TABLE events (
    dt          TEXT PRIMARY KEY,
    campaign_id INTEGER NOT NULL,
    status      TEXT NOT NULL CHECK (status IN ('success', 'failure')),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);
"""
    )

    # --- sample_data.sql (from your PDF) ---
    sample_sql = sql_dir / "sample_data.sql"
    sample_sql.write_text(
        """-- sample_data.sql

-- ============================
-- Customers
-- ============================
INSERT INTO customers (id, first_name, last_name) VALUES
(1, 'Whitney', 'Ferrero'),
(2, 'Dickie', 'Romera');

-- ============================
-- Campaigns
-- ============================
INSERT INTO campaigns (id, customer_id, name) VALUES
(1, 1, 'Upton Group'),
(2, 1, 'Roob, Hudson and Rippin'),
(3, 1, 'McCullough, Rempel and Larson'),
(4, 1, 'Lang and Sons'),
(5, 2, 'Ruecker, Hand and Haley');

-- ============================
-- Clicks (events)
-- ============================
INSERT INTO events (dt, campaign_id, status) VALUES
('2021-12-02 13:52:00', 1, 'failure'),
('2021-12-02 08:17:48', 2, 'failure'),
('2021-12-02 08:18:17', 2, 'failure'),
('2021-12-01 11:55:32', 3, 'failure'),
('2021-12-01 06:53:16', 4, 'failure'),
('2021-12-02 04:51:09', 4, 'failure'),
('2021-12-01 06:34:04', 5, 'failure'),
('2021-12-02 03:21:18', 5, 'failure'),
('2021-12-01 03:18:24', 5, 'failure'),
('2021-12-02 15:32:37', 1, 'success'),
('2021-12-01 04:23:20', 1, 'success'),
('2021-12-02 06:53:24', 1, 'success'),
('2021-12-02 08:01:02', 2, 'success'),
('2021-12-01 15:57:19', 2, 'success'),
('2021-12-02 16:14:34', 3, 'success'),
('2021-12-02 21:56:38', 3, 'success'),
('2021-12-01 05:54:43', 4, 'success'),
('2021-12-02 17:56:45', 4, 'success'),
('2021-12-02 11:56:50', 4, 'success'),
('2021-12-02 06:08:20', 5, 'success');
"""
    )

    # --- applicant_query.sql: returns customers with >3 failures (matching PDF) ---
    query_sql = sql_dir / "applicant_query.sql"
    query_sql.write_text(
        """-- applicant_query.sql
SELECT
    c.first_name || ' ' || c.last_name AS customer,
    COUNT(*) AS failures
FROM customers c
JOIN campaigns cp ON cp.customer_id = c.id
JOIN events e ON e.campaign_id = cp.id
WHERE LOWER(TRIM(e.status)) = 'failure'
GROUP BY c.id, c.first_name, c.last_name
HAVING COUNT(*) > 3
ORDER BY failures DESC, customer ASC;
"""
    )

    return sql_dir


# ---------------------------
# Tests
# ---------------------------

def test_connect_and_test_connection(temp_db_path):
    """
    connect() and test_connection() should work with DB_PATH set to a temp file.
    """
    # connect() should return a sqlite3.Connection
    conn = databaseDAO.connect()
    assert isinstance(conn, sqlite3.Connection)
    conn.close()

    # test_connection should be True
    assert databaseDAO.test_connection() is True


def test_create_and_populate_then_query(temp_db_path, temp_sql_dir):
    """
    Use the DAO internals to run schema and sample_data on a connection,
    then use run_applicant_query to execute the applicant_query.sql and validate output.
    """
    # Step 1: create schema & populate using DAO low-level helper _run_sql_file
    conn = databaseDAO.connect()
    try:
        # Use the DAO helper to run schema and sample data
        databaseDAO._run_sql_file(conn, temp_sql_dir / "schema.sql")
        databaseDAO._run_sql_file(conn, temp_sql_dir / "sample_data.sql")
    finally:
        conn.close()

    # Step 2: execute the applicant_query.sql via DAO public helper
    result_rows = databaseDAO.run_applicant_query(str(temp_sql_dir / "applicant_query.sql"))

    # Expect Whitney Ferrero only (6 failures), per sample_data.txt from PDF
    assert isinstance(result_rows, list)
    assert len(result_rows) == 1

    row0 = result_rows[0]
    # sqlite3.Row allows dict-like access
    assert row0["customer"] == "Whitney Ferrero"
    assert int(row0["failures"]) == 6


def test_execute_query_direct(temp_db_path, temp_sql_dir):
    """
    Verify execute_query returns expected rows for a simple select after schema/data load.
    """
    # Prepare DB
    conn = databaseDAO.connect()
    try:
        databaseDAO._run_sql_file(conn, temp_sql_dir / "schema.sql")
        databaseDAO._run_sql_file(conn, temp_sql_dir / "sample_data.sql")
    finally:
        conn.close()

    # Use execute_query to select customers
    rows = databaseDAO.execute_query("SELECT id, first_name, last_name FROM customers ORDER BY id;")
    assert len(rows) == 2
    assert rows[0]["first_name"] == "Whitney"
    assert rows[1]["first_name"] == "Dickie"
