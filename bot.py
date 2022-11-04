#!/usr/bin/python3

import sqlite3
import os
import telebot
import config

bot = telebot.TeleBot(config.TOKEN)



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


def create_food_table():
    '''
    Create food table in database
    '''
    query = '''CREATE TABLE IF NOT EXISTS food (
                    date TEXT NOT NULL,
                    who TEXT NOT NULL,
                    type TEXT NOT NULL);'''
    db_exec(query)


def get_food_orders():
    '''
    Fetch food orders from database
    '''
    query = f'''SELECT * FROM (SELECT rowid, date, who, type from food ORDER BY rowid DESC LIMIT 10) ORDER BY rowid ASC;'''
    return db_fetch(query)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['orders'])
def food_orders(message):
    bot.reply_to(message, str(get_food_orders()))

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

def main():
    create_food_table()
    print(get_food_orders())
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "main menu"),
        telebot.types.BotCommand("/help", "print usage")
        ]
    )
    bot.infinity_polling()


main()
