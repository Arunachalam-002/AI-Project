# data_loader.py
import pandas as pd

def load_data(filepath="data/TATAMOTORS.csv"):
    df = pd.read_csv(filepath)

    # Clean column names
    df.columns = [c.strip() for c in df.columns]
    df.columns = [c.replace(' ', '') for c in df.columns]

    # Rename common NSE names
    if 'ClosePrice' in df.columns:
        df.rename(columns={'ClosePrice': 'Close'}, inplace=True)
    if 'Date' not in df.columns:
        # fallback: try to find anything with 'date'
        for c in df.columns:
            if 'date' in c.lower():
                df.rename(columns={c: 'Date'}, inplace=True)
                break

    if 'Date' not in df.columns or 'Close' not in df.columns:
        raise ValueError("CSV must contain Date and ClosePrice/Close columns.")

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date']).sort_values('Date')
    df.set_index('Date', inplace=True)
    df = df.reset_index().set_index('Date')  # ensure index is datetime
    return df
