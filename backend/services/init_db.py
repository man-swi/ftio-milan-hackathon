from backend.services.database import get_connection

conn = get_connection()

cursor = conn.cursor()

# -----------------------------------
# TRENDS TABLE
# -----------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trend_name TEXT,
    momentum REAL,
    confidence REAL,
    category TEXT,
    peak_prediction_days INTEGER
)
""")

# -----------------------------------
# INVENTORY TABLE
# -----------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT,
    product_name TEXT,
    category TEXT,
    stock INTEGER,
    sales_velocity TEXT,
    unit_price REAL
)
""")

# -----------------------------------
# MATCHES TABLE
# -----------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trend_name TEXT,
    sku TEXT,
    stock_status TEXT,
    estimated_revenue_impact REAL
)
""")

# -----------------------------------
# HISTORICAL TRENDS TABLE
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
# ANALYSIS HISTORY TABLE
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
# INVENTORY SNAPSHOTS TABLE
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
# RECOMMENDATION HISTORY TABLE
# -----------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS recommendation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_output TEXT,
    reflection_output TEXT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

conn.close()

print("FTIO database initialized successfully.")