#!/usr/bin/python3

from ast import pattern
from email import message
import telebot
from datetime import date
import config
import modules.db as db
import modules.table as tb

############################### Keyboards ############################################
USER_COMMANDS = {
    0: "🛒 Who should order today?",
    1: "🍽 Add today's order (user will be calculated)",
    2: "🛍 List 10 last orders",
    -1: "❌ Cancel",
}

ADMIN_COMMANDS = {
    0: "👥 Show users in food rotation",
    1: "❇️ Add new user to food rotation",
    -1: "❌ Cancel",
}

def keyboard_setup(commands_list, prefix):
    markup = telebot.types.InlineKeyboardMarkup()
    for cmd in commands_list.items():
        markup.add(telebot.types.InlineKeyboardButton(cmd[1], callback_data=f"{prefix}_{cmd[0]}"))
    return markup

############################### Bot ############################################
bot = telebot.TeleBot(config.TOKEN)

############################### Messages ############################################
@bot.message_handler(commands=['start', 'bot'])
def main_menu(message):
    bot.send_message(message.chat.id,
                    f'Howdy, how are you doing? Ima ready for some work',
                    reply_markup = keyboard_setup(USER_COMMANDS, 'user')
                    )
    # bot.register_next_step_handler(msg, user_menu)



@bot.message_handler(commands=['settings'])
def admin_menu(message):
    bot.send_message(message.chat.id,
                    f'Change settings carefully!',
                    reply_markup = keyboard_setup(ADMIN_COMMANDS, 'admin')
                    )
    # bot.register_next_step_handler(msg, admin_menu)


############################### Handlers ############################################
@bot.callback_query_handler(func=lambda call: 'user' in call.data)
def user_menu(call):
    menu_item = call.data.split("_")[-1]
    message = call.message
    match int(menu_item):
        case 0:
            msg = bot.send_message(message.chat.id, f"{who_will_order()} should make the order")
        case 1:
            msg = bot.send_message(message.chat.id, f"{who_will_order()} is making order and it is (choose one type):")
            bot.register_next_step_handler(msg, add_order)
        case 2:
            table = tb.form_table(['id', 'date', 'ordered by', 'type'], db.get_food_orders())
            bot.send_message(message.chat.id, f"<pre>{table}</pre>", 'HTML')
        case _:
            pass
    bot.edit_message_reply_markup(message.chat.id, message.id)


@bot.callback_query_handler(func=lambda call: 'admin' in call.data)
def admin_menu(call):
    menu_item = call.data.split("_")[-1]
    message = call.message
    match int(menu_item):
        case 0:
            table = tb.form_table(['id', 'username'], db.get_users())
            bot.send_message(message.chat.id, f"<pre>{table}</pre>", 'HTML')
        case 1:
            msg = bot.send_message(message.chat.id, 'Enter username of your teammate:')
            bot.register_next_step_handler(msg, add_user_helper)
        case _:
            pass
    bot.edit_message_reply_markup(message.chat.id, message.id)


############################### Functions ############################################
def add_user_helper(message):
    username = message.text
    if '@' in username:
        msg = bot.send_message(message.chat.id, '✅ User name received. Adding to DB')
        db.add_user(username)
    # elif '/cancel' in username:
    #     bot.send_message(message.chat.id, 'Cancelling')
    else:
        bot.send_message(message.chat.id, '❌ Username should starts with symbol @. Cancelling')
        # To infinity retrying uncomment lines below
        # msg = bot.send_message(message.chat.id, 'Username should starts with symbol @. Try again pls')
        # bot.register_next_step_handler(msg, add_user_helper) 


def who_will_order():
    orders = db.get_food_orders(1)
    last_user = orders[0][2] if len(orders) > 0 else ""
    users = [user[1] for user in db.get_users(1000)]
    user_idx = 0
    for user in users:
        if last_user == user:
            current_user_idx = users.index(user)
            user_idx = current_user_idx + 1 if current_user_idx < len(users)-1 else 0
    return users[user_idx]
    

def add_order(message):
    user = who_will_order()
    todays_date = date.today().strftime('%d.%m.%Y')
    db.add_food_order([todays_date, user, ''])


def main():
    db.create_tables()
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Call food bot"),
        telebot.types.BotCommand("/bot", "Another way to call bot"),
        telebot.types.BotCommand("/settings", "Adjust bot settings (like users in rotation)"),
        ]
    )
    bot.infinity_polling()

############################# Launch #########################################
main()
