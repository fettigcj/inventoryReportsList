import pandas as pd
import os
from datetime import datetime, timedelta

# Ensure data directory exists
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
    print(f"Created {DATA_DIR} directory")

# Create sample data
def create_sample_data(filename, num_rows=10):
    """Create a sample Excel file with random data."""
    # Create a DataFrame with sample data
    data = {
        'ID': list(range(1, num_rows + 1)),
        'Name': [f'Item {i}' for i in range(1, num_rows + 1)],
        'Value': [i * 10 for i in range(1, num_rows + 1)],
        'Status': ['Active' if i % 2 == 0 else 'Inactive' for i in range(1, num_rows + 1)]
    }
    df = pd.DataFrame(data)

    # Save to Excel
    df.to_excel(filename, index=False)
    print(f"Created {filename}")

# Create current and historical files for each report type
def create_test_files():
    """Create test files for each report type."""
    # Environment and report types
    environment = "cloud"
    report_types = {
        'Inventory': 'PanInventory',
        'Overrides': 'overrides',
        'Panorama State': 'PanoState',
        'Security Profiles & Groups': 'SecurityProfilesAndGroups'
    }

    # Current date
    today = datetime.now()

    # Create files for each report type
    for report_name, report_key in report_types.items():
        # Current report
        current_filename = f"{environment}_{report_key}.xlsx"
        file_path = os.path.join(DATA_DIR, current_filename)
        create_sample_data(file_path)

        # Historical reports (last 3 days)
        for i in range(1, 4):
            date = today - timedelta(days=i)
            date_str = date.strftime("%y-%m-%d")
            historical_filename = f"{environment}_{report_key}-{date_str}.xlsx"
            file_path = os.path.join(DATA_DIR, historical_filename)
            create_sample_data(file_path)

if __name__ == "__main__":
    create_test_files()
    print("Test data created successfully!")
