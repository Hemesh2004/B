import pandas as pd
import json

# Load dataset
df = pd.read_csv("hotel_bookings.csv")

# Filter: Canceled bookings (is_canceled == 1)
canceled_bookings = df[df["is_canceled"] == 1]

# Group cancellations by arrival date
cancellations_by_date = (
    canceled_bookings.groupby(['arrival_date_year', 'arrival_date_month', 'arrival_date_day_of_month'])
    .size()
    .reset_index(name='cancellations')
)

# Convert to list of dicts for easy JSON export
cancellation_list = cancellations_by_date.to_dict(orient='records')

# Save to JSON
with open("d:/Work/src/cancellations_by_date.json", "w") as f:
    json.dump(cancellation_list, f, indent=4)

print("Non-mathematical analytics (cancellations by date) saved to cancellations_by_date.json")
