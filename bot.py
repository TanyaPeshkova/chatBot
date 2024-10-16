
import telebot

API_TOKEN = '7817016998:AAE2pO153_RxxsQ2KIxzAVLL5ofZBbJ7rEk'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Как я могу помочь Вам?")

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