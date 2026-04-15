import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Create data directories if they don't exist
os.makedirs("data/raw", exist_ok=True)

# ---------------------------------------------------------
# 1. Generate Asset Database (Configuration Items - CIs)
# ---------------------------------------------------------
def generate_assets(num_assets=500):
    ci_types = ['Server', 'Database', 'API Endpoint', 'Network Switch']
    environments = ['Pre-Live', 'Live', 'Assurance']
    
    data = {
        'ci_id': [f"CI-{1000 + i}" for i in range(num_assets)],
        'ci_type': [random.choice(ci_types) for _ in range(num_assets)],
        'environment': [random.choice(environments) for _ in range(num_assets)],
        # Simulate missing owners (Data Quality Issue for HMRC to care about)
        'owner_email': [f"admin_{random.randint(1, 20)}@hmrc.gov.uk" if random.random() > 0.15 else np.nan for _ in range(num_assets)],
        'last_audited': [(datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d') for _ in range(num_assets)]
    }
    
    df_assets = pd.DataFrame(data)
    df_assets.to_csv("data/raw/asset_database.csv", index=False)
    print("✅ Created Asset Database with intentional missing owners.")
    return df_assets

# ---------------------------------------------------------
# 2. Generate Service Tickets (Simulating Pre-Live to Live Transitions)
# ---------------------------------------------------------
def generate_tickets(asset_ids, num_tickets=1000):
    stages = ['Pre-Live Transition', 'Live Incident', 'Assurance Check']
    
    data = []
    for i in range(num_tickets):
        stage = random.choice(stages)
        start_date = datetime.now() - timedelta(days=random.randint(1, 100))
        
        # Simulate "Friction Points": Pre-Live Transitions take much longer for Databases
        if stage == 'Pre-Live Transition' and random.random() > 0.7:
            resolution_days = random.randint(15, 45) # Friction point (Bottleneck)
        else:
            resolution_days = random.randint(1, 5)   # Normal operation
            
        end_date = start_date + timedelta(days=resolution_days)
        
        data.append({
            'ticket_id': f"INC-{5000 + i}",
            'ci_id': random.choice(asset_ids),
            'stage': stage,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'resolution_date': end_date.strftime('%Y-%m-%d'),
            # Simulate inconsistent data entry (Data Quality Issue)
            'status': random.choice(['Resolved', 'Closed', 'Done', 'Fixed']) 
        })
        
    df_tickets = pd.DataFrame(data)
    df_tickets.to_csv("data/raw/service_tickets.csv", index=False)
    print("✅ Created Service Tickets with intentional bottlenecks (friction points).")

# Run the generator
if __name__ == "__main__":
    print("Generating simulated HMRC Service Data...")
    assets_df = generate_assets()
    generate_tickets(assets_df['ci_id'].tolist())
    print("Data generation complete. Check the 'data/raw/' folder.")