#!/usr/bin/python3

from ntpath import join
import telebot
from datetime import date
import config
import modules.db as db
import modules.table as tb

############################### Keyboards ############################################
USER_COMMANDS = {
    0: "🛒❓ Who should order today?",
    1: "🍽 Add today's order (user will be calculated)",
    2: "🛍 List 10 last orders",
    -1: "❌ Cancel",
}

ADMIN_COMMANDS = {
    0: "👥 Show users in food rotation",
    1: "❇️ Add new user to food rotation",
    2: "🍱 Show food types",
    3: "🍳 Add new food type",
    -1: "❌ Cancel",
}


def keyboard_setup(commands_list, prefix):
    markup = telebot.types.InlineKeyboardMarkup()
    for cmd in commands_list.items():
        markup.add(telebot.types.InlineKeyboardButton(cmd[1], callback_data=f"{prefix}_{cmd[0]}"))
    return markup


def food_types_kb(types_list, row_width=1):
    markup = telebot.types.InlineKeyboardMarkup()
    buttons_list = []
    for type in types_list.items():
        buttons_list.append(telebot.types.InlineKeyboardButton(type[1], callback_data=f"food_type_{type[0]}"))
    buttons_list.append(telebot.types.InlineKeyboardButton("❌ Cancel", callback_data="food_type_-1"))
    markup.add(*buttons_list)
    markup.row_width = row_width
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


@bot.message_handler(commands=['settings'])
def admin_menu(message):
    bot.send_message(message.chat.id,
                    f'Change settings carefully!',
                    reply_markup = keyboard_setup(ADMIN_COMMANDS, 'admin')
                    )


############################### Handlers ############################################
@bot.callback_query_handler(func=lambda call: 'user' in call.data)
def user_menu(call):
    menu_item = call.data.split("_")[-1]
    message = call.message
    match int(menu_item):
        case 0:
            bot.send_message(message.chat.id, f"{who_will_order()} should make next order")
        case 1:
            bot.send_message(message.chat.id, 
                            f"{who_will_order()} is making order and it is (choose one type):",
                            reply_markup = food_types_kb(db.get_food_types(), 3))
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
        case 2:
            table = tb.form_table(['type'], db.get_food_types(True))
            bot.send_message(message.chat.id, f"<pre>{table}</pre>", 'HTML')
        case 3:
            msg = bot.send_message(message.chat.id, 'Enter new food type:')
            bot.register_next_step_handler(msg, db.add_food_type)
        case _:
            pass
    bot.edit_message_reply_markup(message.chat.id, message.id)


@bot.callback_query_handler(func=lambda call: 'food_type' in call.data)
def food_types_menu(call):
    menu_item = call.data.split("_")[-1]
    message = call.message
    match int(menu_item):
        case -1:
            bot.edit_message_reply_markup(message.chat.id, message.id)
            bot.send_message(message.chat.id, 'Cancel adding')
        case _:
            food_type = db.get_specific_food_type(int(menu_item))
            add_order(food_type)
            bot.edit_message_reply_markup(message.chat.id, message.id)
            bot.send_message(message.chat.id, 'Successfully added')
            return

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
        # For infinity retrying uncomment lines below
        # msg = bot.send_message(message.chat.id, 'Username should starts with symbol @. Try again pls')
        # bot.register_next_step_handler(msg, add_user_helper) 


def who_will_order():
    orders = db.get_food_orders(1)
    if not orders:
        users = db.get_users()
        if not users:
            return "None"
        return users[0][1]
    last_user = orders[0][2] if len(orders) > 0 else ""
    users = [user[1] for user in db.get_users(1000)]
    user_idx = 0
    for user in users:
        if last_user == user:
            current_user_idx = users.index(user)
            user_idx = current_user_idx + 1 if current_user_idx < len(users)-1 else 0
    return users[user_idx]
    

def add_order(food_type):
    user = who_will_order()
    todays_date = date.today().strftime('%d.%m.%Y')
    db.add_food_order([todays_date, user, food_type])


def main():
    db.create_tables()
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Call food bot"),
        telebot.types.BotCommand("/settings", "Adjust bot settings (like users in rotation)"),
        ]
    )
    bot.infinity_polling()

############################# Launch #########################################
main()
