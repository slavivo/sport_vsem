import re
from flask_app import add_sample

def add_entries_from_file(file_path):
    with open(file_path, 'r') as file:
        entry = {'district': 'jihocesky'}
        for line in file:
            line = line.strip()
            if line.startswith('Pohybové aktivity'):
                entry['activities'] = line.split(': ')[1]
            elif line.startswith('Webová stránka'):
                entry['webpage'] = line.split(': ')[1]
            elif line.startswith('Kontaktní osoba'):
                entry['contact'] = line.split(': ')[1]
            elif line.startswith('Telefon'):
                entry['tel'] = line.split(': ')[1]
            elif line.startswith('Email'):
                entry['email'] = line.split(': ')[1]
            elif line.startswith('Adresa'):
                entry['address'] = line.split(': ')[1]
            elif re.match(r'^\s*$', line):  # Empty line
                if 'address' in entry:
                    add_sample(entry)
                    entry = {'district': 'jihocesky'}
            else:
                entry['name'] = line
        # Add the last entry if it wasn't added
        if entry and 'address' in entry:
            add_sample(entry)

add_entries_from_file('samples.txt')