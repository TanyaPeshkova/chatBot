
import telebot

API_TOKEN = '7817016998:AAE2pO153_RxxsQ2KIxzAVLL5ofZBbJ7rEk'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать!")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Как я могу вам помочь?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == '__main__':
    bot.polling()