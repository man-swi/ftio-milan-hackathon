from database import get_connection

conn = get_connection()
cursor = conn.cursor()

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

cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trend_name TEXT,
    sku TEXT,
    stock_status TEXT,
    estimated_revenue_impact REAL
)
""")

conn.commit()
conn.close()

print("Database initialized successfully.")