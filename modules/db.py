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

def db_exec(query):
    '''
    Executing database query
    '''
    with DbConnect() as sql_connection:
        db_connection, cursor = sql_connection
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
    print(username)

# def add_evening_entry(dpi_list):
#     '''
#     Add entry to the database
#     '''
#     for dpi in dpi_list:
#         # add each dpi as individual line
#         dpi_initial_query = f'''INSERT OR IGNORE INTO {TABLE_NAME} ('{DPI_NAME_COLUMN}', '{LAST_IMPORTED_FOLDER_COLUMN}', '{LAST_IMPORTED_CDR_FOLDER_COLUMN}')
#                     VALUES ('{dpi}', '1970-01-01', '1970-01-01 12:00:00');'''
#         with DbConnect() as sql_connection:
#             db_connection, cursor = sql_connection
#             cursor.execute(dpi_initial_query)
#             db_connection.commit()
