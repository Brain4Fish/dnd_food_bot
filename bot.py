#!/usr/bin/python3

import telebot
from telebot import types
from datetime import date
import config
import modules.db as db
import modules.table as tb

bot = telebot.TeleBot(config.TOKEN)

USER_COMMANDS = {
    0: "🛒 Who should order today?",
    1: "🍽 Add today's order",
    2: "🛍 List 10 last orders",
    100: "❌ Cancel",
}

ADMIN_COMMANDS = {
    100: "❌ Cancel",
}

@bot.message_handler(commands=['start', 'bot'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id,
                    f'Howdy, how are you doing? Ima ready for some work',
                    reply_markup = bot_keyboard_setup(USER_COMMANDS)
                    )
    bot.register_next_step_handler(msg, user_menu)

def bot_keyboard_setup(commands_list):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for cmd in commands_list.items():
        markup.add(telebot.types.KeyboardButton(f"{cmd[0]} - {cmd[1]}"))
    return markup

def user_menu(message):
    match int(message.text.split("-")[0]):
        case 0:
            msg = bot.send_message(
                message.chat.id, f"{who_will_order()} should make the order")
                # reply_markup = bot_keyboard_setup(USER_COMMANDS))
        case 1:
            msg = bot.send_message(message.chat.id, f"{who_will_order()} is making order and it is (choose one type):")
            bot.register_next_step_handler(msg, add_order)
        case 2:
            table = tb.form_table(['id', 'date', 'ordered by', 'type'], db.get_food_orders())
            msg = bot.send_message(message.chat.id, f"<pre>{table}</pre>", 'HTML')
        case _:
            msg = bot.send_message(message.chat.id, "Cancelling")
    bot.register_next_step_handler(msg, user_menu)

# @bot.message_handler(commands=['orders'])
# def food_orders(message):
#     table = tb.form_table(['id', 'date', 'ordered by', 'type'], db.get_food_orders())
#     bot.send_message(message.chat.id, f"<pre>{table}</pre>", 'HTML')

# @bot.message_handler(commands=['users'])
# def bot_get_users(message):
#     table = tb.form_table(['id', 'username'], db.get_users())
#     bot.send_message(message.chat.id, f"<pre>{table}</pre>", 'HTML')

# @bot.message_handler(commands=['add_user'])
# def bot_add_user(message):
#     msg = bot.send_message(message.chat.id, 'Enter username of your teammate (/cancel to cancel operation):')
#     bot.register_next_step_handler(msg, add_user_helper)

# @bot.message_handler(commands=['who'])
# def bot_who(message):
#     bot.reply_to(message, f"{who_will_order()} should make the order")

# @bot.message_handler(commands=['ordered'])
# def bot_ordered(message):
#     add_order(message)


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


def who_will_order():
    orders = db.get_food_orders(1)
    last_user = orders[0][2] if len(orders) > 0 else ""
    users = db.get_users(1000)
    user_id = 0

    for user in users:
        if last_user in user[1]:
            user_id = user[0]
    # Increase user id counter to find who will order next
    user_id += 1
    if user_id > len(users):
        print("Lap ended. Start from the beginning!")
        user_id = 0
    return users[0][1]
    

def add_order(message):
    user = who_will_order()
    todays_date = date.today().strftime('%d.%m.%Y')
    db.add_food_order([todays_date, user, 'Wok'])
    # markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    # users = db.get_users(1000)
    # if not users:
    #     return
    # for user in users:
    #     markup.add(types.KeyboardButton(user[1]))
    # bot.send_message(message.chat.id, "Choose, who ordered food today:", reply_markup=markup)
    # bot.edit_message_reply_markup(reply_markup=None)


def main():
    db.create_tables()
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Call food bot"),
        telebot.types.BotCommand("/bot", "Another way to call bot"),
        ]
    )
    bot.infinity_polling()

main()
