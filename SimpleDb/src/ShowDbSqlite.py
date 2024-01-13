'''
This is the interface to an SQLite Database
'''

import sqlite3

class ShowDbSqlite:
    def __init__(self, dbName='Shows.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Shows (
                showTitle TEXT PRIMARY KEY,
                date TEXT,
                genre TEXT,
                status TEXT,
                rating TEXT
                star_rating TEXT)''')
        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Shows (
                date TEXT PRIMARY KEY,
                showTitle TEXT,
                genre TEXT,
                status TEXT,
                status TEXT,
                rating TEXT
                star_rating TEXT)''')
        self.commit_close()

    def fetch_shows(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Shows')
        shows =self.cursor.fetchall()
        self.conn.close()
        return shows

    def insert_show(self, date, showTitle, genre, status, rating, star_rating):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO Shows (date, showTitle, genre, status, rating, star_rating) VALUES (?, ?, ?, ?, ?, ?)',
                    (date, showTitle,genre,  status, rating, star_rating))
        self.commit_close()

    def delete_show(self, showTitle):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM Shows WHERE showTitle = ?', (showTitle,))
        self.commit_close()

    def update_show(self, new_date, new_genre, new_status, new_rating, new_star_rating, showTitle):
        self.connect_cursor()
        self.cursor.execute('UPDATE Shows SET date = ?, genre = ?, status = ?, rating = ?, star_rating = ? WHERE showTitle = ?',
                    (new_date,new_genre, new_status,  new_rating, new_star_rating, showTitle))
        self.commit_close()

    def id_exists(self, showTitle):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM Shows WHERE showTitle = ?', (showTitle,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            dbEntries = self.fetch_shows()
            for entry in dbEntries:
                print(entry)
                filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]},{entry[5]}\n")
