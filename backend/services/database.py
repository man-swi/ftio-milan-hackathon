import sqlite3

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "ftio.db"


# -----------------------------------
# CONNECTION
# -----------------------------------

def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# -----------------------------------
# INITIALIZE DATABASE
# -----------------------------------

def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    # -----------------------------------
    # HISTORICAL TRENDS
    # -----------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historical_trends (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        trend_name TEXT,

        momentum REAL,

        confidence REAL,

        category TEXT,

        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -----------------------------------
    # ANALYSIS HISTORY
    # -----------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        total_revenue_opportunity REAL,

        total_inventory_risk REAL,

        average_confidence REAL,

        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -----------------------------------
    # INVENTORY SNAPSHOTS
    # -----------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory_snapshots (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        sku TEXT,

        product_name TEXT,

        stock INTEGER,

        risk_level TEXT,

        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -----------------------------------
    # RECOMMENDATION HISTORY
    # -----------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recommendation_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        strategy_output TEXT,

        reflection_output TEXT,

        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -----------------------------------
    # STRATEGY MEMORY
    # -----------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS strategy_memory (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        strategy_text TEXT,

        recorded_at TEXT
    )
    """)

    # -----------------------------------
    # REFLECTION MEMORY
    # -----------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reflection_memory (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        reflection_text TEXT,

        recorded_at TEXT
    )
    """)

    conn.commit()

    conn.close()

    print("DATABASE INITIALIZED")


# -----------------------------------
# SAVE HISTORICAL TRENDS
# -----------------------------------

def save_historical_trends(trends):

    conn = get_connection()

    cursor = conn.cursor()

    for trend in trends:

        cursor.execute("""
        INSERT INTO historical_trends (
            trend_name,
            momentum,
            confidence,
            category
        )
        VALUES (?, ?, ?, ?)
        """, (

            trend["trend"],
            trend["momentum"],
            trend["confidence"],
            trend["category"]

        ))

    conn.commit()

    conn.close()


# -----------------------------------
# SAVE ANALYSIS HISTORY
# -----------------------------------

def save_analysis_history(metrics):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO analysis_history (
        total_revenue_opportunity,
        total_inventory_risk,
        average_confidence
    )
    VALUES (?, ?, ?)
    """, (

        metrics["total_revenue_opportunity"],
        metrics["total_inventory_risk"],
        metrics["average_confidence"]

    ))

    conn.commit()

    conn.close()


# -----------------------------------
# SAVE INVENTORY SNAPSHOTS
# -----------------------------------

def save_inventory_snapshots(alerts):

    conn = get_connection()

    cursor = conn.cursor()

    for alert in alerts:

        cursor.execute("""
        INSERT INTO inventory_snapshots (
            sku,
            product_name,
            stock,
            risk_level
        )
        VALUES (?, ?, ?, ?)
        """, (

            alert.get("sku", "UNKNOWN"),
            alert["product"],
            alert["current_stock"],
            alert["priority"]

        ))

    conn.commit()

    conn.close()


# -----------------------------------
# SAVE RECOMMENDATION HISTORY
# -----------------------------------

def save_recommendation_history(
    strategy_output,
    reflection_output
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO recommendation_history (
        strategy_output,
        reflection_output
    )
    VALUES (?, ?)
    """, (

        strategy_output,
        reflection_output

    ))

    conn.commit()

    conn.close()


# -----------------------------------
# GET PREVIOUS TREND
# -----------------------------------

def get_previous_trend(trend_name):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM historical_trends
    WHERE trend_name = ?
    ORDER BY recorded_at DESC
    LIMIT 1 OFFSET 1
    """, (trend_name,))

    result = cursor.fetchone()

    conn.close()

    return result


# -----------------------------------
# GET LATEST ANALYSIS
# -----------------------------------

def get_latest_analysis():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM analysis_history
    ORDER BY recorded_at DESC
    LIMIT 1
    """)

    result = cursor.fetchone()

    conn.close()

    return result