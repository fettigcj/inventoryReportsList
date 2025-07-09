from flask import Flask, render_template, send_file, redirect, url_for
import os
import glob
import re
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# Report types and their file patterns
REPORT_TYPES = {
    'Inventory': 'PanInventory',
    'Overrides': 'overrides',
    'Panorama State': 'PanoState',
    'Security Profiles & Groups': 'SecurityProfilesAndGroups'
}

def get_report_files():
    """Get all Excel report files in the data directory."""
    excel_files = glob.glob('data/*.xlsx')
    # Return just the filenames without the 'data/' prefix for compatibility
    return [os.path.basename(file) for file in excel_files]

def categorize_reports(files):
    """Categorize reports by type and separate current from historical."""
    reports = {report_type: {'current': None, 'historical': []} for report_type in REPORT_TYPES.values()}

    for file in files:
        # Check if this is a report file
        for report_name, report_key in REPORT_TYPES.items():
            if report_key in file:
                # Extract the environment (part before underscore)
                match = re.match(r'([^_]+)_', file)
                if match:
                    environment = match.group(1)

                    # Check if this is a current or historical report
                    if re.search(r'-\d{2}-\d{2}-\d{2}\.xlsx$', file):  # Has date suffix
                        reports[report_key]['historical'].append({
                            'filename': file,
                            'environment': environment,
                            'date': re.search(r'-(\d{2}-\d{2}-\d{2})\.xlsx$', file).group(1)
                        })
                    else:  # Current report
                        reports[report_key]['current'] = {
                            'filename': file,
                            'environment': environment
                        }
                break

    # Sort historical reports by date (newest first)
    for report_type in reports:
        reports[report_type]['historical'].sort(
            key=lambda x: datetime.strptime(x['date'], '%y-%m-%d'), 
            reverse=True
        )

    return reports

@app.route('/')
def index():
    """Main page - list all report types and their files."""
    files = get_report_files()
    reports = categorize_reports(files)

    return render_template('index.html', 
                          reports=reports, 
                          report_types=REPORT_TYPES)

@app.route('/view/<filename>')
def view_report(filename):
    """View the contents of a report."""
    try:
        # Read the Excel file from the data directory
        file_path = os.path.join('data', filename)

        # Get all sheet names
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names

        # Read each sheet and convert to HTML table
        sheets_data = {}
        for sheet_name in sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            # Convert to HTML table with DataTables classes
            table_html = df.to_html(classes='table table-striped table-bordered display', index=False)
            sheets_data[sheet_name] = table_html

        # Default to the first sheet
        active_sheet = sheet_names[0] if sheet_names else None

        return render_template('view.html', 
                              filename=filename, 
                              sheets_data=sheets_data,
                              sheet_names=sheet_names,
                              active_sheet=active_sheet)
    except Exception as e:
        return f"Error viewing file: {str(e)}"

@app.route('/historical/<report_key>')
def historical_reports(report_key):
    """Show historical reports for a specific report type."""
    files = get_report_files()
    reports = categorize_reports(files)

    # Find the report name corresponding to the report key
    report_name = next((name for name, key in REPORT_TYPES.items() if key == report_key), "Unknown")

    # Get historical reports for the specified report type
    historical_reports = reports.get(report_key, {}).get('historical', [])

    return render_template('historical.html',
                          report_name=report_name,
                          historical_reports=historical_reports)

@app.route('/download/<filename>')
def download_report(filename):
    """Download a report file."""
    try:
        file_path = os.path.join('data', filename)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return f"Error downloading file: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
