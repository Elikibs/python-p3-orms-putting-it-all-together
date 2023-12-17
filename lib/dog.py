import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    # Initializing instance attributes
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed
    
