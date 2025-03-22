from fastapi import FastAPI, HTTPException
import sqlite3
from typing import List, Dict

app = FastAPI()

DB_PATH = "d:/Work/src/analytics.db"
CANCELLATIONS_JSON = "d:/Work/src/cancellations_by_date.json"

# Function to fetch analytics from SQLite
def get_analytics_from_db() -> Dict:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Revenue trend
    cursor.execute("SELECT month, revenue FROM revenue_trend")
    revenue_trend = {month: revenue for month, revenue in cursor.fetchall()}

    # Cancellation rate
    cursor.execute("SELECT rate FROM cancellation_rate WHERE id=1")
    cancellation_rate_row = cursor.fetchone()
    cancellation_rate = cancellation_rate_row[0] if cancellation_rate_row else "0%"

    # Geo distribution
    cursor.execute("SELECT country, bookings FROM geo_distribution")
    geo_distribution = {country: bookings for country, bookings in cursor.fetchall()}

    # Lead time distribution
    cursor.execute("SELECT metric, value FROM lead_time_distribution")
    lead_time_distribution = {metric: value for metric, value in cursor.fetchall()}

    conn.close()

    return {
        "revenue_trend": revenue_trend,
        "cancellation_rate": cancellation_rate,
        "geo_distribution": geo_distribution,
        "lead_time_distribution": lead_time_distribution
    }

@app.get("/")
def root():
    return {"message": "Hotel Booking Analytics API is running!"}

@app.post("/analytics")
def get_analytics():
    analytics = get_analytics_from_db()
    return analytics

@app.get("/cancellations_by_date")
def get_cancellations(year: int, month: str, day: int):
    import json

    # Load precomputed JSON data
    with open(CANCELLATIONS_JSON, "r") as f:
        cancellations = json.load(f)

    # Filter for the requested date
    for entry in cancellations:
        if (entry["arrival_date_year"] == year and
            entry["arrival_date_month"].lower() == month.lower() and
            entry["arrival_date_day_of_month"] == day):
            return entry

    raise HTTPException(status_code=404, detail="No cancellations found for this date")
