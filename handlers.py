import telebot
from telebot import types
from datetime import datetime
import pytz
import requests
from config import API_TOKEN
from utils import get_timezone_by_city, get_exchange_rate

# bot = telebot.TeleBot(API_TOKEN)

def send_welcome(bot, message):
    bot.reply_to(message, "Добро пожаловать! Как я могу помочь Вам?")
    
    show_main_menu(message)


def show_main_menu(bot, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    date = types.KeyboardButton("Узнать дату и время")
    currency = types.KeyboardButton("Конвертация валюты")
    markup.add(date,currency)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)


def ask_region(bot, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes_button = types.KeyboardButton("Да")
    no_button = types.KeyboardButton("Нет")
    markup.add(yes_button, no_button)
    bot.send_message(message.chat.id, "Вы из Томской области?", reply_markup=markup)


def handle_region_response(bot, message):
    if message.text == "Да":
        tomsk_tz = pytz.timezone('Asia/Tomsk')
        local_time = datetime.now(tomsk_tz).strftime("%Y-%m-%d %H:%M:%S")
        bot.send_message(message.chat.id, f"Местная дата и время в Томске: {local_time}")
    else:
        bot.send_message(message.chat.id, "Введите ваш город:")
        bot.register_next_step_handler(message, get_city_time,bot)

def get_city_time( message, bot):
    city = message.text
    timezone = get_timezone_by_city(city)
    if timezone:
        city_tz = pytz.timezone(timezone)
        current_time = datetime.now(city_tz).strftime("%Y-%m-%d %H:%M:%S")
        bot.send_message(message.chat.id, f"Местная дата и время в {city}: {current_time}")
    else:
        bot.send_message(message.chat.id, "Не удалось определить временную зону для указанного города. Пожалуйста, проверьте название города.")
    
    show_main_menu(bot, message)

def ask_from_currency(message, bot):
    bot.send_message(message.chat.id, "Введите валюту, из которой хотите перевести сумму (например, RUB):")
    bot.register_next_step_handler(message, ask_to_currency, bot)

def ask_to_currency(message, bot):
    from_currency = message.text.upper()
    bot.send_message(message.chat.id, "Введите валюту, в которую хотите перевести сумму (например, USD):")
    bot.register_next_step_handler(message, lambda msg, bot=bot: ask_amount(msg, from_currency,bot),bot)

def ask_amount(message, from_currency,bot):
    to_currency = message.text.upper()
    bot.send_message(message.chat.id, "Введите сумму для конвертации:")
    bot.register_next_step_handler(message, lambda msg, bot=bot: convert_currency(msg, from_currency, to_currency, bot))

def convert_currency(message, from_currency, to_currency, bot):
    try:
        amount = float(message.text)
        rate = get_exchange_rate(from_currency, to_currency)
        
        if rate:
            converted_amount = amount * rate
            bot.send_message(message.chat.id, f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
        else:
            bot.send_message(message.chat.id, "Не удалось получить курс валют. Пожалуйста, проверьте валюты.")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат. Пожалуйста, введите сумму числом.")
    
    show_main_menu(bot, message)


def send_help(message, bot):
    bot.reply_to(message, "Как я могу вам помочь?")


def echo_all(message, bot):
    user_message = message.text.lower()

    if 'как дела' in user_message or 'как ты' in user_message:
        bot.reply_to(message, "У меня всё отлично, спасибо! А у Вас?")
    elif 'что делаешь' in user_message or 'чем занимаешься' in user_message:
        bot.reply_to(message, "Я здесь, чтобы помочь Вам! А Вы чем занимаетесь?")
    elif 'привет' in user_message or 'здравствуй' in user_message:
        bot.reply_to(message, "Здавствуйте! Как я могу помочь Вам?")
    elif 'пока' in user_message or 'до свидания' in user_message:
        bot.reply_to(message, "До свидания!")    
    else:
        bot.reply_to(message, "Извините, я Вас не понимю")
