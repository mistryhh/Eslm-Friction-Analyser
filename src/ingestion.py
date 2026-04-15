import pandas as pd
import os

# Ensure the processed directory exists
os.makedirs("data/processed", exist_ok=True)

def load_raw_data():
    """Loads the raw simulated datasets."""
    print("📥 Loading raw data from 'data/raw/'...")
    assets = pd.read_csv("data/raw/asset_database.csv")
    tickets = pd.read_csv("data/raw/service_tickets.csv")
    return assets, tickets

def clean_asset_data(df):
    """Audits and cleans the Configuration Item (CI) database."""
    print("🧹 Auditing Asset Database (Configuration Items)...")
    
    # 1. ESLM Data Quality Check: Flag missing owners
    missing_owners_count = df['owner_email'].isna().sum()
    print(f"   -> WARNING: Found {missing_owners_count} CIs missing an owner email.")
    
    # 2. Impute missing data (Standardizing the structure)
    df['owner_email'] = df['owner_email'].fillna('UNASSIGNED_REQUIRES_AUDIT')
    
    return df

def clean_ticket_data(df):
    """Standardises service ticket data for analysis."""
    print("🧹 Standardising Service Tickets...")
    
    # 1. ESLM Consistency Check: Standardize messy status inputs
    status_mapping = {
        'Resolved': 'Closed',
        'Done': 'Closed',
        'Fixed': 'Closed',
        'Closed': 'Closed'
    }
    df['status_standardised'] = df['status'].map(status_mapping).fillna(df['status'])
    
    # 2. Convert date strings to actual DateTime objects
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['resolution_date'] = pd.to_datetime(df['resolution_date'])
    
    return df

def run_ingestion_pipeline():
    """Executes the full ingestion and cleaning pipeline."""
    print("🚀 Starting HMRC Data Ingestion Pipeline...")
    
    # Load
    raw_assets, raw_tickets = load_raw_data()
    
    # Transform / Clean
    cleaned_assets = clean_asset_data(raw_assets)
    cleaned_tickets = clean_ticket_data(raw_tickets)
    
    # Save Output
    cleaned_assets.to_csv("data/processed/cleaned_assets.csv", index=False)
    cleaned_tickets.to_csv("data/processed/cleaned_tickets.csv", index=False)
    
    print("✅ Pipeline Complete! Cleaned data saved to 'data/processed/'.")

if __name__ == "__main__":
    run_ingestion_pipeline()