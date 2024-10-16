import telebot
from telebot import types
from datetime import datetime
import pytz 
import requests

API_TOKEN = '7817016998:AAE2pO153_RxxsQ2KIxzAVLL5ofZBbJ7rEk'
OPENCAGE_API_KEY = '6e7c559dbdb24eea901e3a7a8a3e9c7f'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Как я могу помочь Вам?")
    show_main_menu(message)

def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Узнать дату и время")
    markup.add(item)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Узнать дату и время")
def ask_region(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes_button = types.KeyboardButton("Да")
    no_button = types.KeyboardButton("Нет")
    markup.add(yes_button, no_button)
    bot.send_message(message.chat.id, "Вы из Томской области?", reply_markup=markup)
@bot.message_handler(func=lambda message: message.text in ["Да", "Нет"])
def handle_region_response(message):
    if message.text == "Да":
        tomsk_tz = pytz.timezone('Asia/Tomsk')
        local_time = datetime.now(tomsk_tz).strftime("%Y-%m-%d %H:%M:%S")
        bot.send_message(message.chat.id, f"Местная дата и время в Томске: {local_time}")
    else:
        bot.send_message(message.chat.id, "Введите ваш город:")
        bot.register_next_step_handler(message, get_city_time)

def get_city_time(message):
    city = message.text
    timezone = get_timezone_by_city(city)
    if timezone:
        city_tz= pytz.timezone(timezone)
        current_time = datetime.now(city_tz).strftime("%Y-%m-%d %H:%M:%S")
        bot.send_message(message.chat.id, f"Местная датавремя в {city}: {current_time}")
    else:
        bot.send_message(message.chat.id, "Не удалось определить временную зону для указанного города. Пожалуйста, проверьте название города.")

    show_main_menu(message)
    

def get_timezone_by_city(city):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={OPENCAGE_API_KEY}&language=ru"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            timezone = data['results'][0]['annotations']['timezone']['name']
            return timezone
    return None

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Как я могу вам помочь?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_message = message.text.lower()

    if 'как дела' in user_message:
        bot.reply_to(message, "У меня всё отлично, спасибо! А у Вас?")
    elif 'что делаешь' in user_message or 'чем занимаешься' in user_message:
        bot.reply_to(message, "Я здесь, чтобы помочь Вам! А Вы чем занимаетесь?")
    elif 'привет' in user_message or 'здравствуй' in user_message:
        bot.reply_to(message, "Здавствуйте! Как я могу помочь Вам?")
    elif 'пока' in user_message or 'до свидания' in user_message:
        bot.reply_to(message, "До свидания!")    
    else:
        bot.reply_to(message, "Извините, я Вас не понимю")
if __name__ == '__main__':
    bot.polling()