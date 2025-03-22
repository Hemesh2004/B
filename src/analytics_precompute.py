import json
import sqlite3

# Load analytics from JSON file
with open("d:/Work/src/analytics.json", "r") as f:
    analytics = json.load(f)

# Connect to SQLite database (creates one if it doesn't exist)
conn = sqlite3.connect("d:/Work/src/analytics.db")
cursor = conn.cursor()

# Create tables for each analytic
cursor.execute("""
CREATE TABLE IF NOT EXISTS revenue_trend (
    month TEXT PRIMARY KEY,
    revenue REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cancellation_rate (
    id INTEGER PRIMARY KEY,
    rate TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS geo_distribution (
    country TEXT PRIMARY KEY,
    bookings INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS lead_time_distribution (
    metric TEXT PRIMARY KEY,
    value REAL
)
""")

# Insert revenue_trend
cursor.execute("DELETE FROM revenue_trend")
for month, revenue in analytics["revenue_trend"].items():
    cursor.execute("INSERT INTO revenue_trend (month, revenue) VALUES (?, ?)", (month, revenue))

# Insert cancellation_rate
cursor.execute("DELETE FROM cancellation_rate")
cursor.execute("INSERT INTO cancellation_rate (id, rate) VALUES (?, ?)", (1, analytics["cancellation_rate"]))

# Insert geo_distribution
cursor.execute("DELETE FROM geo_distribution")
for country, bookings in analytics["geo_distribution"].items():
    cursor.execute("INSERT INTO geo_distribution (country, bookings) VALUES (?, ?)", (country, bookings))

# Insert lead_time_distribution
cursor.execute("DELETE FROM lead_time_distribution")
for metric, value in analytics["lead_time_distribution"].items():
    cursor.execute("INSERT INTO lead_time_distribution (metric, value) VALUES (?, ?)", (metric, value))

# Commit changes and close connection
conn.commit()
conn.close()

print("Analytics successfully saved to SQLite database (analytics.db)")
