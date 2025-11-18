-- schema.sql
-- Schema for Challenge 3: Advertising System Failures Report

--DROP TABLE IF EXISTS customers;
--DROP TABLE IF EXISTS campaigns;
--DROP TABLE IF EXISTS events;

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
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ============================
-- Table: clicks
-- ============================
CREATE TABLE events (
    dt          TEXT PRIMARY KEY,
    campaign_id INTEGER NOT NULL,
    status      TEXT NOT NULL CHECK (status IN ('success', 'failure')),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id)
);
