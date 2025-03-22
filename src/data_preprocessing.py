import pandas as pd

def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)

    # Basic Cleaning
    df['country'].fillna('Unknown', inplace=True)
    df['agent'].fillna(0, inplace=True)
    df['company'].fillna(0, inplace=True)
    
    # Date conversion
    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])

    # Add calculated fields
    df['total_stay'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    df['revenue'] = df['adr'] * df['total_stay']
    df['year_month'] = df['reservation_status_date'].dt.to_period('M')

    return df

if __name__ == "__main__":
    df = load_and_clean_data('data/hotel_bookings.csv')
    print(df.head())
