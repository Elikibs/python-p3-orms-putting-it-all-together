import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    # Initializing instance attributes
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed
    

    # 'create_table' class method that creates 'dogs' table in our database
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs(
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)

    # 'drop_table' class method deletes table 'dogs' if it exists
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(sql)