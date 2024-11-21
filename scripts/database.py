import sqlite3
from datetime import datetime, timedelta
import os
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Root directory
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'spotify_plays.db')
BACKUP_DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'csv_backups')

class DatabaseManager:
    def __init__(self, database_path = DATABASE_PATH, backup_path = BACKUP_DATABASE_PATH):
        self.database_path = database_path
        self.backup_path = backup_path
        self.check_database()

    def backup_to_csv(self):
        # Create a timestamped folder for this backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(self.backup_path, f"backup_{timestamp}")
        os.makedirs(backup_folder, exist_ok=True)

        # Connect to the database
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        # Retrieve all table names in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for (table_name,) in tables:
            # Export each table to a CSV file
            self._export_table_to_csv(cursor, table_name, backup_folder)

        conn.close()
        print(f"Database successfully backed up to CSV in folder: {backup_folder}")

    def _export_table_to_csv(self, cursor, table_name, backup_folder):
        # Query all data from the table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Get column names for the CSV header
        column_names = [description[0] for description in cursor.description]

        # Define CSV file path
        csv_file_path = os.path.join(backup_folder, f"{table_name}.csv")

        # Write to CSV
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerow(column_names)  # Write header
            writer.writerows(rows)         # Write data rows

        print(f"Table {table_name} exported to {csv_file_path}")

    def check_and_backup(self):
        # Ensure the backup directory exists
        if not os.path.exists(self.backup_path):
            os.makedirs(self.backup_path)

        if self.is_database_empty():
            print("Database is empty. No backup needed.")
            return

        # Retrieve backup files in the backup directory
        backup_files = [
            f for f in os.listdir(self.backup_path)
            if f.startswith("backup_")
        ]

        # Determine the timestamp of the latest backup
        if backup_files:
            latest_backup_file = max(
                backup_files,
                key=lambda f: datetime.strptime(f[7:-3], "%Y%m%d_%H%M%S")
            )
            last_backup_time = datetime.strptime(latest_backup_file[7:-3],
                                                 "%Y%m%d_%H%M%S")
        else:
            last_backup_time = None  # No backups found

        # Check if a new backup is needed
        if last_backup_time is None or datetime.now() - last_backup_time > timedelta(
                hours=168):
            print("Performing a backup on application startup.")
            self.backup_to_csv()

    def is_database_empty(self):
        """Check if the database contains any records."""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM plays")
            count = cursor.fetchone()[0]
            conn.close()
            return count == 0  # True if the table is empty

        except sqlite3.Error as e:
            print(f"Error checking if database is empty: {e}")
            return True  # Assume empty if there's an error

    def insert_play(self, track_id, track_name, artist, album, year, duration_ms, explicit, popularity, played_at, session_id=None):
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO plays (track_id, track_name, artist, album, year, duration_ms, explicit, popularity, played_at, session_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (track_id, track_name, artist, album, year, duration_ms, explicit, popularity, played_at, session_id))

        conn.commit()
        conn.close()

    def get_recent_plays(self, limit=50):
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        # Query to select the most recent plays, excluding consecutive duplicates
        cursor.execute('''
        SELECT track_id, track_name, artist, played_at
        FROM plays
        ORDER BY played_at DESC
        LIMIT ?
        ''', (limit,))

        plays = cursor.fetchall()
        conn.close()

        # Filter out consecutive duplicates
        filtered_plays = []
        last_track_id = None

        for play in plays:
            if play[0] != last_track_id:
                filtered_plays.append(play)
                last_track_id = play[0]

        return filtered_plays

    def get_most_recent_play_timestamp(self):
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        cursor.execute("SELECT MAX(played_at) FROM plays")
        latest_played_at = cursor.fetchone()[0]
        conn.close()

        # Convert to datetime if it exists and is not None
        if latest_played_at:
            latest_played_at = datetime.strptime(latest_played_at,
                                                 "%Y-%m-%d %H:%M:%S.%f")
        return latest_played_at

    def check_database(self):
        # Check if the database dir exists
        database_dir = os.path.dirname(self.database_path)
        if not os.path.exists(database_dir):
            os.makedirs(database_dir)
            print(f"Created directory for database at {database_dir}")

        # Creates a new table if one does not exist
        self._create_table()
        print("Database check complete.")

    def _create_table(self):
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS plays (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        track_id TEXT NOT NULL,
        track_name TEXT NOT NULL,
        artist TEXT NOT NULL,
        album TEXT,               
        year INTEGER,             
        duration_ms INTEGER,      
        explicit BOOLEAN,         
        popularity INTEGER,       
        played_at TIMESTAMP NOT NULL,
        session_id TEXT
    )
    ''')

        conn.commit()
        conn.close()
