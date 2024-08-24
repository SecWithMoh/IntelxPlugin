import json
import sqlite3
import subprocess
import os
import shutil
from typing import Dict

# Function to create a table based on the fields in a record
def create_table_if_not_exists(cursor, table_name: str, fields: Dict, unique_key: str):
    columns = ['"ID" INTEGER PRIMARY KEY AUTOINCREMENT']  # Add the ID field
    for key, value in fields.items():
        if isinstance(value, int):
            if abs(value) > 9223372036854775807:  # Maximum 64-bit signed integer
                columns.append(f'"{key}" TEXT')
            else:
                columns.append(f'"{key}" INTEGER')
        elif isinstance(value, float):
            columns.append(f'"{key}" REAL')
        elif isinstance(value, bool):
            columns.append(f'"{key}" BOOLEAN')
        elif isinstance(value, (list, dict)):
            columns.append(f'"{key}" TEXT')
        else:
            columns.append(f'"{key}" TEXT')

    # Add unique constraint to the unique_key column
    columns_definition = ", ".join(columns) + f', UNIQUE("{unique_key}")'
    create_table_query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns_definition})'
    cursor.execute(create_table_query)

# Function to insert a record into a table using INSERT OR IGNORE
def insert_record(cursor, table_name: str, fields: Dict):
    keys = ", ".join([f'"{key}"' for key in fields.keys()])
    placeholders = ", ".join(["?" for _ in fields])
    
    # Serialize complex types (like lists and dicts) to JSON strings
    values = tuple(
        json.dumps(value) if isinstance(value, (list, dict)) else 
        (str(value) if isinstance(value, int) and abs(value) > 9223372036854775807 else value)
        for value in fields.values()
    )
    
    # Use INSERT OR IGNORE to prevent inserting duplicates
    insert_query = f'INSERT OR IGNORE INTO "{table_name}" ({keys}) VALUES ({placeholders})'
    cursor.execute(insert_query, values)

# Function to move .bin files to the output directory
def move_bin_files_to_output(output_dir):
    for file_name in os.listdir("."):
        if os.path.isfile(file_name) and file_name.endswith(".bin"):
            # Move .bin file to the output directory
            shutil.move(file_name, os.path.join(output_dir, file_name))

# Function to save the last processed ID to a file
def save_last_id(last_id, file_name="last_id.txt"):
    with open(file_name, 'w') as file:
        file.write(str(last_id))

# Function to load the last processed ID from a file
def load_last_id(file_name="last_id.txt"):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return int(file.read().strip())
    return None

# Function to execute the external command for each record in the database
def execute_commands_from_db(db_name: str, apikey: str, output_dir: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Retrieve all ID, systemid, and bucket values from the database
    cursor.execute("SELECT ID, systemid, bucket FROM records")
    rows = cursor.fetchall()

    # Load the last processed ID
    last_id = load_last_id()

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Run the command for each row
    for row in rows:
        record_id, systemid, bucket = row
        
        # Skip rows until we reach the last processed ID
        if last_id and record_id <= last_id:
            continue

        command = ["python3", "intelx.py", "-download", systemid, "-bucket", bucket, "-apikey", apikey, "-media", "24", "-sort", "4"]
        try:
            subprocess.run(command, check=True)
            print(f"Command executed successfully for systemid: {systemid}")

            # Move .bin files to the output directory
            move_bin_files_to_output(output_dir)

            # Save the last processed ID
            save_last_id(record_id)

        except subprocess.CalledProcessError as e:
            print(f"Error executing command for systemid: {systemid}, error: {e}")
            break  # Stop processing further if an error occurs

    conn.close()

# Main function to process JSON and save to database
def process_json_to_db(file_name: str, db_name: str, unique_key: str, apikey: str, output_dir: str):
    try:
        # Read the JSON file
        with open(file_name, 'r') as file:
            data = json.load(file)
        
        # Connect to the SQLite database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Process each record
        for record in data["records"]:
            # Create table based on the record's fields with a unique constraint
            create_table_if_not_exists(cursor, "records", record, unique_key)
            # Insert the record into the table
            insert_record(cursor, "records", record)
            
        # Commit changes and close the database connection
        conn.commit()
        conn.close()

        # Execute commands for all records in the database
        execute_commands_from_db(db_name, apikey, output_dir)
    
    except KeyboardInterrupt:
        print("\nProcess interrupted by user (Ctrl+C). Exiting program...")
    except Exception as e:
        print(f"An error occurred: {e}")

# Get the JSON file name, API key, and output directory from the user
file_name = input("Enter the JSON file name: ")
apikey = input("Enter the API key: ")
output_dir = input("Enter the output directory: ")

# Call the main function with the JSON file, database name, API key, and output directory
process_json_to_db(file_name, "data_records.db", "systemid", apikey, output_dir)
