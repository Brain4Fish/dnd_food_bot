#!/usr/bin/python3

import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.set_my_commands([
    telebot.types.BotCommand("/start", "main menu"),
    telebot.types.BotCommand("/help", "print usage")
    ]
)

bot.infinity_polling()
