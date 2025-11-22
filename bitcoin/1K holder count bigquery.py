from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
from datetime import datetime, timedelta



creds = service_account.Credentials.from_service_account_file('/Users/user/keys/quickstart-1565992709235-4309e921b030.json')

# --- Setup client ---
client = bigquery.Client(credentials=creds)

# --- Parameters ---
DATASET = "bigquery-public-data.crypto_bitcoin.outputs"
START_DATE = datetime(2009, 1, 3)   # Genesis block
END_DATE = datetime(2025, 1, 1)
BTC_THRESHOLD = 1000                # addresses with ≥ 1000 BTC
MAX_SCAN_GB = 0.5                   # skip queries over 0.5 GB (adjust as needed)

def make_query(start, end):
    """Return query string for one week."""
    return f"""
    SELECT
      DATE_TRUNC(DATE(block_timestamp), WEEK(MONDAY)) AS week_start,
      COUNT(DISTINCT addr) AS whale_addresses
    FROM (
      SELECT
        o.value / 1e8 AS btc_value,
        o.block_timestamp,
        addr
      FROM `{DATASET}` AS o
      CROSS JOIN UNNEST(o.addresses) AS addr
      WHERE o.block_timestamp BETWEEN TIMESTAMP('{start}') AND TIMESTAMP('{end}')
        AND o.value / 1e8 >= {BTC_THRESHOLD}
    )
    GROUP BY week_start
    ORDER BY week_start
    """

results = []
current = START_DATE

while current < END_DATE:
    next_week = current + timedelta(days=7)
    query = make_query(current.strftime("%Y-%m-%d"), next_week.strftime("%Y-%m-%d"))

    # --- Dry run to check scan size ---
    dry_job = client.query(query)
    scanned = 0 if dry_job.total_bytes_processed == None else dry_job.total_bytes_processed
    gb_scanned = scanned / 1e9
    print(f"{current:%Y-%m-%d} → {next_week:%Y-%m-%d}: {gb_scanned:.2f} GB to scan")

    if gb_scanned <= MAX_SCAN_GB:
        df = client.query(query).to_dataframe()
        if not df.empty:
            results.append(df)
    else:
        print("⚠️ Skipped to stay under free-tier limit")

    current = next_week

# --- Combine results ---
if results:
    final_df = pd.concat(results)
    final_df.sort_values("week_start", inplace=True)
    final_df.reset_index(drop=True, inplace=True)
    final_df.to_csv("btc_whale_addresses_weekly.csv", index=False)
    print("✅ Saved btc_whale_addresses_weekly.csv")
else:
    print("No data collected (all weeks skipped).")