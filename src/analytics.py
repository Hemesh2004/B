import pandas as pd
import json

# Load dataset
df = pd.read_csv("hotel_bookings.csv")  # ✅ Your path

# Compute Analytics
revenue_trend = (
    df.groupby('arrival_date_month')['adr']
    .sum()
    .sort_index()
    .to_dict()
)

total_bookings = len(df)
total_cancellations = df['is_canceled'].sum()
cancellation_rate = (total_cancellations / total_bookings) * 100

geo_distribution = df['country'].value_counts().head(10).to_dict()

lead_time_distribution = df['lead_time'].describe().to_dict()

# Prepare analytics dictionary
analytics_result = {
    "revenue_trend": revenue_trend,
    "cancellation_rate": f"{cancellation_rate:.2f}%",
    "geo_distribution": geo_distribution,
    "lead_time_distribution": lead_time_distribution
}

# Save to JSON
with open(r"d:\Work\src\analytics.json", "w") as f:
    json.dump(analytics_result, f, indent=4)

print("Analytics successfully saved to analytics.json")
