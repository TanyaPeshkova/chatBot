from telebot import types
from datetime import datetime
import pytz
from utils import *
from responses import responses

def send_welcome(bot, message):
    bot.reply_to(message, "Добро пожаловать! Как я могу помочь Вам?")
    show_main_menu(bot,message)


def show_main_menu(bot, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        types.KeyboardButton("Узнать дату и время"),
        types.KeyboardButton("Конвертация валюты"),
        types.KeyboardButton("Узнать погоду"),
        types.KeyboardButton("Найти в интернете") ,
    ]
    
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)


def ask_region(bot, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes_button = types.KeyboardButton("Да")
    no_button = types.KeyboardButton("Нет")
    markup.add(yes_button, no_button)
    bot.send_message(message.chat.id, "Вы из Томской области?", reply_markup=markup)
    bot.register_next_step_handler(message, handle_region_response, bot)


def handle_region_response(message, bot):
    if message.text == "Да":
        send_local_time(bot, message, "Томск", "Asia/Tomsk")
        
        show_main_menu(bot, message)
    else:
        bot.send_message(message.chat.id, "Введите ваш город:")
        bot.register_next_step_handler(message, get_city_time, bot)

def get_city_time( message, bot):
    city = message.text
    timezone = get_timezone_by_city(city)
    if timezone:
        send_local_time(bot, message, city, timezone)
    else:
        bot.send_message(message.chat.id, "Не удалось определить временную зону для указанного города. Пожалуйста, проверьте название города.")
    
    show_main_menu(bot, message)


def send_local_time(bot, message, city, timezone):
    city_tz = pytz.timezone(timezone)
    current_time = datetime.now(city_tz).strftime("%Y-%m-%d %H:%M:%S")
    bot.send_message(message.chat.id, f"Местная дата и время в {city}: {current_time}")


def ask_from_currency(bot, message):
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


def ask_city(bot, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes_button = types.KeyboardButton("Да")
    no_button = types.KeyboardButton("Нет")
    markup.add(yes_button, no_button)
    bot.send_message(message.chat.id, "Узнать погоду в Томске?", reply_markup=markup)
    bot.register_next_step_handler(message, handle_waether_response, bot)


def handle_waether_response( message, bot):
    if message.text == "Да":
        send_weather_info(bot, message, "Томск")
    else:
        bot.send_message(message.chat.id, "Введите ваш город:")
        bot.register_next_step_handler(message, get_city_weather, bot)
    

def get_city_weather( message, bot):
    city = message.text
    send_weather_info(bot, message, city)

def send_weather_info(bot, message, city):
    weather_info = get_weather(city)
    if weather_info:
        bot.send_message(message.chat.id, weather_info)
    else:
        bot.send_message(message.chat.id, "Не удалось получить данные о погоде. Пожалуйста, проверьте название города.")
    
    show_main_menu(bot, message)

def ask_query(bot, message):
    bot.send_message(message.chat.id, "Введите ваш запрос")
    bot.register_next_step_handler(message, handle_google_search, bot)


def handle_google_search(message, bot):
    query = message.text
    google_info = search_google(query)
    bot.reply_to(message, google_info)

def send_help(message, bot):
    help_text = (
        "Этот чат-бот может:\n"
        "1. Узнать местное время в Томске или в любом другом регионе мира.\n"
        "2. Конвертировать валюты.\n"
        "3. Узнать погоду в Томске или любом другом городе мира.\n"
        "4. Найти информацию в интернете."
    )
    bot.reply_to(message, help_text)


def echo_all(message, bot):
    user_message = message.text.lower()

    for key in responses:
        if key in user_message:
            bot.reply_to(message, responses[key])
            return
    bot.reply_to(message, "Извините, я Вас не понимаю")
