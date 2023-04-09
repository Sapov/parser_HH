import sqlite3
import time

db = '2h.db'


class Database:

    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

    def add_table(self):
        with self.connection:
            res = self.cursor.execute('''CREATE TABLE hh (
            id INTEGER PRIMARY KEY,
            title TEXT,
            link TEXT,
            vacancy_description TEXT,
            company TEXT,
            salary TEXT,
            description TEXT,
            add_date datetime
            );''')

    def add_base(self, response: dict):
        try:
            with self.connection:
                return self.cursor.execute(f"""INSERT INTO hh
                              (title, link, salary, vacancy_description, company, description)
                              VALUES
                              ('{response['title']}', '{response['link']}', '{response['salary']}', '{response['vacancy_description']}', 
                              '{response['company']}', '{response['description']}');""")
        except:
            print('ERROR')

    def select_experience(self):
        with self.connection:
            self.cursor.execute(f'''SELECT * FROM hh WHERE vacancy_description = "Требуемый опыт работы: не требуется"''')
            records = self.cursor.fetchall()
            print("Вывод ID ", id)
            for row in records:
                print("ID:", row[0])
                print("Title:", row[1])
                print("Link:", row[2])
                print("Experience:", row[3])
                print("Company:", row[4])
                print("Selery:", row[5])
                print("Description:", row[6], end="\n\n")

if __name__ == '__main__':
    # Database(db).add_table()
    Database(db).select_experience()
