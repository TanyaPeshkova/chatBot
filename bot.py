import telebot
from telebot import types
from datetime import datetime
import pytz 
import requests
from config import API_TOKEN

from handlers import *

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    send_welcome(bot, message)

@bot.message_handler(func=lambda message: message.text == "Узнать дату и время")
def handle_current_date(message):
    ask_region(bot, message)

@bot.message_handler(func=lambda message: message.text in ["Да", "Нет"])
def handle_region(message):
    handle_region_response(bot, message)


@bot.message_handler(func=lambda message: message.text == "Конвертация валюты")
def handle_currency_change(message):
    ask_from_currency(bot, message)

@bot.message_handler(func=lambda message: message.text == "Узнать погоду")
def handle_weather(message):
    ask_city( bot,message)

@bot.message_handler(func=lambda message: message.text in ["Да", "Нет"])
def handle_city(message):
    handle_waether_response( bot,message)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Как я могу вам помочь?")


@bot.message_handler(func=lambda message: True)
def handle_echo(message):
    echo_all(message, bot)


if __name__ == '__main__':
    bot.polling()