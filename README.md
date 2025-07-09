# Excel Reports Viewer

A Flask application to list Excel files in the 'data' folder, offering users the ability to view the contents of the most recent report or download prior reports found in the app's data directory.

## Report Types

The application supports the following report types:
- Inventory (`cloud_PanInventory.xlsx`)
- Overrides (`cloud_overrides.xlsx`)
- Panorama State (`cloud_PanoState.xlsx`)
- Security Profiles & Groups (`cloud_SecurityProfilesAndGroups.xlsx`)

## File Naming Convention

The file names for each report follow this pattern:
- Current reports: `<environment>_<report_key>.xlsx`
- Historical reports: `<environment>_<report_key>-YY-MM-DD.xlsx`

Where:
- `<environment>` is an identifier (e.g., "cloud")
- `<report_key>` is the key for the report type (e.g., "PanoState")
- `YY-MM-DD` is the date when the report was rotated (e.g., "25-07-07")

Note: A report with date suffix (e.g., "PanoState-25-07-07.xlsx") contains data from the previous day (July 6th, 2025, in this example).

## Installation

1. Clone this repository
2. Create a virtual environment (optional but recommended):
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
   Or install them individually:
   ```
   pip install flask pandas openpyxl setuptools
   ```

## Usage

1. Place your Excel report files in the 'data' folder
   - Make sure the 'data' folder exists in the project root directory
   - For testing, you can generate sample data using the provided script:
     ```
     python test_data.py
     ```
   - This script will create the 'data' folder if it doesn't exist
2. Run the application:
   ```
   python app.py
   ```
3. Open your web browser and navigate to `http://127.0.0.1:5000/`

## Features

- Lists all available reports by type on the home page
- Shows current reports on the home page with links to historical reports
- Displays historical reports on separate pages to reduce clutter
- Allows viewing report contents directly in the browser
- Provides download links for all reports
- Sorts historical reports by date (newest first)
- Uses DataTables for filtering and pagination of report data
- Supports viewing multiple sheets (tabs) in Excel files
- Responsive XLSX viewer that adapts to the user's window width
- Per-column filtering for complex, multi-column data queries
- Vertical scrolling of report content to minimize window movement
- Horizontal scrolling of worksheet tabs to save screen space

## Troubleshooting

### ModuleNotFoundError: No module named '_distutils_hack'

If you encounter this error when running the application, it's related to the setuptools package. To fix it:

1. Make sure you have setuptools installed:
   ```
   pip install --upgrade setuptools
   ```

2. If the error persists, try reinstalling pip:
   ```
   python -m pip install --upgrade pip
   ```

3. In some cases, you might need to reinstall your virtual environment if it's corrupted.

### ValueError: numpy.dtype size changed, may indicate binary incompatibility

If you encounter this error when running the application, it's related to a version mismatch between numpy and pandas. To fix it:

1. Make sure you have the compatible versions specified in requirements.txt:
   ```
   pip install -r requirements.txt
   ```

2. If the error persists, try installing the specific compatible versions manually:
   ```
   pip install numpy==1.24.3 pandas==2.1.0
   ```

3. In some cases, you might need to uninstall and reinstall both packages:
   ```
   pip uninstall -y numpy pandas
   pip install numpy==1.24.3 pandas==2.1.0
   ```
