import sqlite3
import pandas as pd
import xlwings as xw
import os
import psutil
import win32com.client as win32
import pytz

TIMEZONE = "Europe/Helsinki"

# Function to update Excel file with database data
def update_excel():
    # Connect to SQLite database
    conn = sqlite3.connect('database/spotify_plays.db')

    # Query data
    df = pd.read_sql_query("SELECT * FROM plays", conn)

    # Define timezones
    utc = pytz.UTC
    timezone = pytz.timezone(TIMEZONE)

    # Convert played_at to datetime and split into date and time
    df['played_at'] = pd.to_datetime(df['played_at'], utc=True)  # Parse datetime
    df['played_at'] = df['played_at'].dt.tz_convert(timezone)
    df['date'] = pd.to_datetime(df['played_at']).dt.date  # Extract date
    df['time'] = pd.to_datetime(df['played_at']).dt.strftime('%H.%M.%S')

    # Classify time into time of day
    df['time_of_day'] = df['played_at'].dt.hour.map(
        lambda hour: 'Morning' if 5 <= hour < 12 else
        'Afternoon' if 12 <= hour < 17 else
        'Evening' if 17 <= hour < 21 else
        'Night')

    # Specify the Excel file name
    excel_file = os.path.abspath('plays_sheets.xlsx')  # Use absolute path for reliability

    # Open the workbook with xlwings (visible to make sure it fully releases later)
    app = xw.App(visible=False)
    wb = app.books.open(excel_file)

    try:
        # Select the sheet named 'data'
        if 'data' in [sheet.name for sheet in wb.sheets]:
            sheet = wb.sheets['data']
        else:
            # If the 'data' sheet does not exist, add it
            sheet = wb.sheets.add('data')

        # Clear existing content while keeping the header row intact
        sheet.clear_contents()  # This will clear everything but leave slicers and other features intact

        # Write DataFrame to Excel, starting at cell A1
        sheet.range("A1").value = df

        # Save the workbook after writing the data
        wb.save()
    finally:
        wb.close()
        app.quit()

    # Close the database connection
    conn.close()

    # Make sure all Excel processes are killed
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'EXCEL.EXE':
            proc.kill()

    # Create an Excel table using win32com
    create_excel_table(excel_file)

    print("Excel file updated successfully.")

# Function to create an Excel table using win32com.client
def create_excel_table(file_path):
    excel = win32.Dispatch('Excel.Application')
    excel.Visible = False
    try:
        wb = excel.Workbooks.Open(file_path)
        sheet = wb.Sheets('data')

        # Define the table range (assuming data starts at A1)
        last_row = sheet.Cells(sheet.Rows.Count, 1).End(win32.constants.xlUp).Row
        last_column = sheet.Cells(1, sheet.Columns.Count).End(win32.constants.xlToLeft).Column
        table_range = sheet.Range(sheet.Cells(1, 1), sheet.Cells(last_row, last_column))

        # Create a list of existing tables to avoid duplicate creation
        table_names = [tbl.Name for tbl in sheet.ListObjects]
        table_name = "PlaysTable"

        # Remove existing table if it exists
        if table_name in table_names:
            sheet.ListObjects(table_name).Delete()

        # Add the table
        sheet.ListObjects.Add(
            SourceType=win32.constants.xlSrcRange,
            Source=table_range,
            XlListObjectHasHeaders=win32.constants.xlYes
        ).Name = table_name

        # Save the workbook after adding the table
        wb.Save()
    finally:
        wb.Close(SaveChanges=True)
        excel.Application.Quit()

# Function to open the Excel file
def open_excel(file_path):
    try:
        excel = win32.Dispatch('Excel.Application')
        excel.Visible = True  # Make Excel visible
        excel.Workbooks.Open(file_path)  # Open the specified workbook
    except Exception as e:
        print(f"Failed to open Excel file: {e}")

# Main script
if __name__ == "__main__":
    excel_file = os.path.abspath('plays_sheets.xlsx')
    update_excel()  # Update the Excel file
    open_excel(excel_file)  # Open the Excel file
