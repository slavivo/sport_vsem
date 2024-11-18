import sqlite3
import json

def convert_db_to_json():
    # Connect to SQLite database
    conn = sqlite3.connect('instance/site.db')
    cursor = conn.cursor()
    
    # Get all samples from the database
    cursor.execute('SELECT * FROM sample')
    rows = cursor.fetchall()
    
    # Get column names
    column_names = [description[0] for description in cursor.description]
    
    # Convert rows to list of dictionaries
    samples = []
    for row in rows:
        sample = {}
        for i, column in enumerate(column_names):
            sample[column] = row[i]
        samples.append(sample)
    
    # Group samples by district
    samples_by_district = {}
    for sample in samples:
        district = sample['district']
        if district not in samples_by_district:
            samples_by_district[district] = []
        samples_by_district[district].append(sample)
    
    # Write to JSON file
    with open('samples.json', 'w') as file:
        json.dump(samples_by_district, file, indent=4)
    
    conn.close()

if __name__ == '__main__':
    convert_db_to_json()