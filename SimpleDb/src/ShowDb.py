from ShowDbEntry import ShowDbEntry
import json


class ShowDb:
    """
    - simple database to store EmpDbEntry objects
    """    

    def __init__(self, init=False, dbName='ShowDb.csv'):
        """
        - initialize database variables here
        - mandatory :
            - any type can be used to store database entries for EmpDbEntry objects
            - e.g. list of class, list of dictionary, list of tuples, dictionary of tuples etc.
        """
        # CSV filename         
        self.dbName = dbName
        self.entries = []  # Using a list to store EmpDbEntry objects
        if init:
            self.load_csv()
        else:
            pass
        print('TODO: __init__')

    def id_exists(self, showTitle):
        """
        - returns True if an entry exists for the specified 'showTitle'
        - else returns False
        """
        return any(entry.showTitle.lower() == showTitle.lower() for entry in self.entries)
    

    def fetch_shows(self):

        print('TODO: fetch_Shows')
        tupleList = []

        # Append entries from self.entries to tupleList
        tupleList += [(entry.date, entry.showTitle, entry.genre,entry.status, entry.rating, entry.star_rating) for entry in self.entries]

        return tupleList

    def insert_show(self, date, showTitle, genre, status, rating, star_rating):
        """
        - inserts an entry in the database
        - no return value
        """
        newEntry = ShowDbEntry(date=date, showTitle=showTitle, genre=genre, status=status,  rating=rating, star_rating=star_rating)
        self.entries.append(newEntry)
        print('TODO: insert_show')

    def delete_show(self, showTitle):
        """
        - deletes the corresponding entry in the database as specified by 'showTitle'
        - no return value
        """
        self.entries = [entry for entry in self.entries if entry.showTitle != showTitle]
        print('TODO: delete_Show')

    def update_show(self, new_date, new_genre, new_status, new_rating, showTitle, new_star_rating):
        """
        - updates the corresponding entry in the database as specified by 'showTitle'
        - no return value
        """
        for entry in self.entries:
            if entry.showTitle == showTitle:
                entry.date = new_date
                entry.genre = new_genre
                entry.status = new_status
                entry.rating = new_rating
                entry.star_rating = new_star_rating
        print('TODO: update_Show')

    def export_csv(self):

        with open(self.dbName, 'w') as file:
        # Write the entries from self.entries
            for entry in self.entries:
                file.write(f"{entry.date},{entry.showTitle},{entry.genre},{entry.status},{entry.rating},{entry.star_rating}\n")
        print('TODO: export_csv')


    def export_json(self, json_filename='ShowDb.json'):
        data = []

        for entry in self.entries:
            entry_data = {
                'date': entry.date,
                'showTitle': entry.showTitle,
                'genre': entry.genre,
                'status': entry.status,
                'rating': entry.rating,
                'star_rating': entry.star_rating
            }
            data.append(entry_data)

        try:
            with open(json_filename, 'w') as json_file:
                json.dump(data, json_file, indent=2)
            print(f"Database exported to {json_filename} successfully.")
        except Exception as e:
            print(f"Error exporting to JSON: {e}")

    def load_from_csv(self, csv_filename=None):


        
        try:
            self.entries = []
            file_path = csv_filename or self.dbName
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    values = line.strip().split(',')
                    if len(values) == 6:
                        date, showTitle, genre, status, rating, star_rating = values
                        entry = ShowDbEntry(date, showTitle, genre, status, rating, star_rating)
                        self.entries.append(entry)
                    else:
                        print(f"Skipping invalid entry: {line}")
        except FileNotFoundError:
            print(f"File '{self.dbName}' not found. Creating an empty database.")