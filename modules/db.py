import sqlite3
import os

##
# Database functions
##


class DbConnect(object):
    '''
    Creates and closes connection to the database
    '''

    def __init__(self, exec_path = os.path.dirname(os.path.realpath(__file__)), database='bot.db'):
        self.exec_path = exec_path
        self.database = database
        self.dbconn = None

    def __enter__(self):
        '''
        Create database connection

        Returns tuple of two objects: connection and cursor for database access
        '''
        self.dbconn = sqlite3.connect(f'{self.exec_path}/{self.database}')
        return self.dbconn, self.dbconn.cursor()

    def __exit__(self, type, value, traceback):
        '''
        Close database connection
        '''
        if self.dbconn:
            self.dbconn.close()

##
# General DB functions
##

def db_exec(query, bulkdata=None):
    '''
    Executing database query
    '''
    with DbConnect() as sql_connection:
        db_connection, cursor = sql_connection
        if bulkdata:
            cursor.executemany(query, bulkdata)
        else:
            cursor.execute(query)
        db_connection.commit()


def db_fetch(query):
    '''
    Executing database fetch query
    '''
    with DbConnect() as sql_connection:
        _, cursor = sql_connection
        cursor.execute(query)
        selected_data = cursor.fetchall()
    return selected_data

def create_tables():
    print("Initialising databases")
    create_food_table()
    create_users_table()
    create_types_table()
    init_food_types()
    print("Done")

##
# Orders related things
##

def create_food_table():
    '''
    Create food table in database
    '''
    query = '''CREATE TABLE IF NOT EXISTS food (
                    date TEXT NOT NULL,
                    who TEXT NOT NULL,
                    type TEXT NOT NULL);'''
    db_exec(query)


def get_food_orders(limit = 10):
    '''
    Fetch last N food orders from database
    '''
    query = f'''SELECT * FROM (SELECT rowid, date, who, type from food ORDER BY rowid DESC LIMIT {limit}) ORDER BY rowid ASC;'''
    return db_fetch(query)


def add_food_order(data):
    '''
    Add food order to database
    '''
    query = f'''INSERT OR IGNORE INTO food ('date', 'who', 'type')
                  VALUES ('{data[0]}', '{data[1]}', '{data[2]}');'''
    db_exec(query)

##
# User related things
##

def create_users_table():
    '''
    Create users table in database
    '''
    query = '''CREATE TABLE IF NOT EXISTS users (
                    user TEXT NOT NULL);'''
    db_exec(query)


def get_users(limit = 10):
    '''
    Fetch last N users from database
    '''
    query = f'''SELECT * FROM (SELECT rowid, user from users ORDER BY rowid DESC LIMIT {limit}) ORDER BY rowid ASC;'''
    return db_fetch(query)


def add_user(username):
    '''
    Add user to the database
    '''
    check_query = f'''SELECT user FROM users WHERE user = "{username}"'''
    if db_fetch(check_query):
        return "User already exists"
    query = f'''INSERT OR IGNORE INTO users ('user')
                  VALUES ('{username}');'''
    db_exec(query)

##
# Food type related things
##

def create_types_table():
    '''
    Create food types table in database
    '''
    query = '''CREATE TABLE IF NOT EXISTS food_types (type TEXT NOT NULL, UNIQUE(type));'''
    db_exec(query)


def get_food_types(as_table = False):
    '''
    Fetch food types from database
    '''
    query = f'''SELECT type FROM food_types;'''
    result = db_fetch(query)
    if as_table:
        return result
    types = [food[0] for food in result]
    tmp = {}
    for type in types:
        tmp[types.index(type)] = type
    return tmp


def get_specific_food_type(id):
    id += 1 # We need this, because sqlite id's starts from 1
    query = f'''SELECT type FROM food_types WHERE rowid = {id};'''
    return db_fetch(query)[0][0]


def add_food_type(message):
    '''
    Add food type to the database
    '''
    food_type = message.text
    check_query = f'''SELECT type FROM food_types WHERE type = "{food_type}"'''
    if db_fetch(check_query):
        return "Food type already exists"
    query = f'''INSERT OR IGNORE INTO food_types ('type')
                  VALUES ('{food_type}');'''
    db_exec(query)


def init_food_types():
    '''
    Add initial food types
    '''
    types = ['🍔', '🍕', '🌯', '🍜', '🍣']
    query = f'''INSERT OR IGNORE INTO food_types ('type') VALUES (?);'''
    db_exec(query, types)
