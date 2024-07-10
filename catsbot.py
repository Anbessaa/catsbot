import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = '7497254218:AAE2YfsgK1Ir0kJ0N4KwlSDmNjVzajxa5YQ'  # Replace with your real token
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.username
    is_premium = message.from_user.is_premium  # This attribute needs checking if your Telegram API version supports it.
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Let's go", web_app=WebAppInfo(url='https://anbessaa.github.io/catsbot/')))
    
    welcome_message = f"Hello, {username}!\n"
    if is_premium:
        welcome_message += "You have Telegram Premium!\n"
    else:
        welcome_message += "You don't have Telegram Premium.\n"
    welcome_message += "How cool is your Telegram profile? Check your rating and receive rewards."
    
    bot.reply_to(message, welcome_message, reply_markup=markup)

@bot.message_handler(commands=['invite'])
def invite_friends(message):
    bot.reply_to(message, "Invite your friends to join us! https://t.me/blackcat_community")

bot.polling(none_stop=True)
