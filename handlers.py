from telebot import types
from datetime import datetime
import pytz
from utils import *


def send_welcome(bot, message):
    bot.reply_to(message, "Добро пожаловать! Как я могу помочь Вам?")
    show_main_menu(bot,message)


def show_main_menu(bot, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    date = types.KeyboardButton("Узнать дату и время")
    currency = types.KeyboardButton("Конвертация валюты")
    weather = types.KeyboardButton("Узнать погоду")
    search = types.KeyboardButton("Найти в интернете")
    markup.add(date,currency, weather,search)
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
        tomsk_tz = pytz.timezone('Asia/Tomsk')
        local_time = datetime.now(tomsk_tz).strftime("%Y-%m-%d %H:%M:%S")
        bot.send_message(message.chat.id, f"Местная дата и время в Томске: {local_time}")
        show_main_menu(bot, message)
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
        weather_info = get_weather("Томск")
        if weather_info:
            bot.send_message(message.chat.id, weather_info)
        else:
            bot.send_message(message.chat.id, "Не удалось получить данные о погоде. Пожалуйста, проверьте название города.")
        show_main_menu(bot, message)
    else:
        bot.send_message(message.chat.id, "Введите ваш город:")
        bot.register_next_step_handler(message, get_city_weather,bot)
    

def get_city_weather( message, bot):
    city = message.text
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
    if 'как дела' in user_message  or 'как ты' in user_message or 'как настроение' in user_message:
        bot.reply_to(message, "У меня всё отлично, спасибо! А у Вас?")
    elif 'что делаешь' in user_message or 'чем занимаешься' in user_message:
        bot.reply_to(message, "Я здесь, чтобы помочь Вам! А Вы чем занимаетесь?")
    elif 'привет' in user_message  or 'здравствуй' in user_message:
        bot.reply_to(message, "Здавствуйте! Как я могу помочь Вам?")
    elif 'кто ты' in user_message or 'как тебя зовут' in user_message:
        bot.reply_to(message, "Я — ваш виртуальный помощник, созданный для того, чтобы отвечать на ваши вопросы и помогать вам с различными задачами. Чем могу помочь вам сегодня?")
    elif 'пока' in user_message  or 'до свидания' in user_message:
        bot.reply_to(message, "До свидания!\n Надеюсь, я смог Вам помочь!")
    elif 'нравится' in user_message or 'любимый' in user_message:
        bot.reply_to(message, "Как чат-боту, у меня нет 'нравится' в том же смысле, что у человека. 😊 Но мне очень нравится учиться! \n Я люблю получать новую информацию, расширять свои знания и использовать их, чтобы быть полезным. ")
    elif 'у тебя планы' in user_message:
        bot.reply_to(message, "У меня нет планов в том смысле, что у человека, у которого есть желания, мечты и стремления. 😅 \nЯ — большая языковая модель, и моя главная задача — помогать людям. ")
    
    else:
        bot.reply_to(message, "Извините, я Вас не понимаю")
