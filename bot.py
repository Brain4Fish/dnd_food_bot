#!/usr/bin/python3

import telebot
import config
import modules.db as db
import modules.table as tb

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['orders'])
def food_orders(message):
    # bot.reply_to(message, str(db.get_food_orders()))
    table = tb.form_table(['id', 'date', 'ordered by', 'type'], db.get_food_orders())
    bot.send_message(message.chat.id, f"<pre>{table}</pre>", 'HTML')

@bot.message_handler(commands=['users'])
def bot_get_users(message):
    table = tb.form_table(['id', 'username'], db.get_users())
    bot.send_message(message.chat.id, f"<pre>{table}</pre>", 'HTML')

@bot.message_handler(commands=['add_user'])
def bot_add_user(message):
    msg = bot.send_message(message.chat.id, 'Enter username of your teammate (/cancel to cancel operation):')
    bot.register_next_step_handler(msg, add_user_helper)


# add user
def add_user_helper(message):
    username = message.text
    if '@' in username:
        msg = bot.send_message(message.chat.id, 'User name received. Adding to DB')
        db.add_user(username)
    elif '/cancel' in username:
        bot.send_message(message.chat.id, 'Cancelling')
    else:
        msg = bot.send_message(message.chat.id, 'Username should starts with symbol @. Try again pls')
        bot.register_next_step_handler(msg, add_user_helper)

def main():
    db.create_tables()
    bot.set_my_commands([
        telebot.types.BotCommand("/orders", "print last 10 orders"),
        telebot.types.BotCommand("/users", "print your teammates"),
        telebot.types.BotCommand("/add_user", "add your new teammate"),
        ]
    )
    bot.infinity_polling()

main()
