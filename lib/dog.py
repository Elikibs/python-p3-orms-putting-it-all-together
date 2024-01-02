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

    # 'save' instance method that saves a Dog object to your database
    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """

            CURSOR.execute(sql, (self.name, self.breed))
            self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]



    # 'create' class method creates a new instance of Dog Class and then calls on the 'save' method to insert the records to our table
    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    # Mapping from database records to Python objects

    # Getting data from specific table row
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog
        

    # 'get_all' class method returns a list of Dog instances for every record in the dogs table
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * 
            FROM dogs
        """

        # Return array of rows from the db that matches our query
        rows = CURSOR.execute(sql).fetchall()

        # Iterate over each row and use 'new_from_db() to create a new python object for each row.
        dogs_list = [cls.new_from_db(row) for row in rows]
        return dogs_list
    
    # 'find_by_name' class method creates instances for queries matching the 'name' given
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * 
            FROM dogs
            WHERE name = ?
            LIMIT 1
        """

        # Return array of rows from the db that matches our query
        dog = CURSOR.execute(sql, (name,)).fetchone()

        # Create instances for 'dog' above
        return cls.new_from_db(dog)
    
    # 'find_by_id' class method creates instances for queries matching the 'id' given
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM dogs
            WHERE id = ?
            LIMIT 1
        """

        # Return array of rows from the db that matches our query
        dog = CURSOR.execute(sql, (id,)).fetchone()

        # Create instances for 'dog' above
        return cls.new_from_db(dog)
    

    @classmethod
    def find_or_create_by(cls, name, breed):
        # Check if a dog with the provided name and breed already exists
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ? AND breed = ?
            LIMIT 1
        """
        # Return array of rows from the db that matches our query
        existing_dog = CURSOR.execute(sql, (name, breed)).fetchone()

        if existing_dog:
            # If the dog already exists, return it
            return cls.new_from_db(existing_dog)
        else:
            # If the dog does not exist, create and save a new instance
            new_dog = cls.create(name, breed)
            return new_dog
    

    def update(self):
        if self.id is not None:
            # If the Dog instance has an ID, update the corresponding row in the database
            sql = """
                UPDATE dogs
                SET name=?
                WHERE id=?
            """

            CURSOR.execute(sql, (self.name, self.id))



