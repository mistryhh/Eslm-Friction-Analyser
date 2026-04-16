import pandas as pd
import os

# Ensure the insights directory exists
os.makedirs("data/processed", exist_ok=True)

def load_cleaned_data():
    """Loads the standardized datasets."""
    print("📥 Loading cleaned data from 'data/processed/'...")
    assets = pd.read_csv("data/processed/cleaned_assets.csv")
    tickets = pd.read_csv("data/processed/cleaned_tickets.csv")
    
    # Ensure dates are datetime objects after loading from CSV
    tickets['start_date'] = pd.to_datetime(tickets['start_date'])
    tickets['resolution_date'] = pd.to_datetime(tickets['resolution_date'])
    
    return assets, tickets

def calculate_resolution_times(tickets):
    """Calculates how long each ticket took to resolve in days."""
    tickets['resolution_time_days'] = (tickets['resolution_date'] - tickets['start_date']).dt.days
    # Filter out any weird negative values just in case
    tickets = tickets[tickets['resolution_time_days'] >= 0]
    return tickets

def identify_friction_points(tickets, assets):
    """
    Analyses the data to find bottlenecks in ESLM stages, 
    specifically looking at Pre-Live to Live transitions.
    """
    print("\n🔍 ANALYSING FRICTION POINTS...")
    
    # Merge tickets with asset data to see WHICH systems are failing
    merged_data = pd.merge(tickets, assets, on='ci_id', how='left')
    
    # 1. MTTR by ESLM Stage
    stage_mttr = merged_data.groupby('stage')['resolution_time_days'].mean().round(1).reset_index()
    stage_mttr.rename(columns={'resolution_time_days': 'avg_resolution_days'}, inplace=True)
    
    print("\n📊 Average Resolution Time by ESLM Stage:")
    print(stage_mttr.to_string(index=False))
    
    # 2. Deep Dive: Pre-Live Transition Bottlenecks
    pre_live_data = merged_data[merged_data['stage'] == 'Pre-Live Transition']
    bottlenecks = pre_live_data.groupby('ci_type')['resolution_time_days'].mean().round(1).reset_index()
    bottlenecks.rename(columns={'resolution_time_days': 'avg_transition_days'}, inplace=True)
    bottlenecks = bottlenecks.sort_values(by='avg_transition_days', ascending=False)
    
    print("\n⚠️ Pre-Live Transition Bottlenecks by CI Type (Friction Points):")
    print(bottlenecks.to_string(index=False))
    
    return stage_mttr, bottlenecks, merged_data

def run_analysis_pipeline():
    """Executes the analysis pipeline and saves insights."""
    print("🚀 Starting ESLM Analysis...")
    
    assets, tickets = load_cleaned_data()
    tickets = calculate_resolution_times(tickets)
    
    stage_mttr, bottlenecks, enriched_data = identify_friction_points(tickets, assets)
    
    # Save insights for the dashboard to use later
    stage_mttr.to_csv("data/processed/mttr_by_stage.csv", index=False)
    bottlenecks.to_csv("data/processed/prelive_bottlenecks.csv", index=False)
    enriched_data.to_csv("data/processed/enriched_master_data.csv", index=False)
    
    print("\n✅ Analysis Complete! Insight reports saved to 'data/processed/'.")

if __name__ == "__main__":
    run_analysis_pipeline()