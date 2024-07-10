import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from datetime import datetime

TOKEN = '7497254218:AAE2YfsgK1Ir0kJ0N4KwlSDmNjVzajxa5YQ'  # Замените на ваш реальный токен
bot = telebot.TeleBot(TOKEN)

def calculate_cats(is_premium, account_age_years):
    # Базовые токены в зависимости от наличия премиум аккаунта
    base_tokens = 5000 if is_premium else 2500

    # Дополнительные токены в зависимости от возраста аккаунта
    if account_age_years < 1:
        age_tokens = 1000
    elif account_age_years < 2:
        age_tokens = 2000
    else:
        age_tokens = 3000 + (account_age_years - 2) * 1000

    return base_tokens + age_tokens

@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.username
    is_premium = getattr(message.from_user, 'is_premium', False)  # Проверка на наличие атрибута is_premium
    account_creation_date = datetime.fromtimestamp(message.from_user.date)  # Получение даты создания аккаунта
    account_age_years = (datetime.now() - account_creation_date).days // 365  # Расчет возраста аккаунта в годах
    
    cats_tokens = calculate_cats(is_premium, account_age_years)
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Let's go", web_app=WebAppInfo(url='https://anbessaa.github.io/catsbot/')))
    
    welcome_message = f"Hello, {username}!\nYou have {cats_tokens} CATS tokens.\n"
    welcome_message += "How cool is your Telegram profile? Check your rating and receive rewards."
    
    bot.reply_to(message, welcome_message, reply_markup=markup)

@bot.message_handler(commands=['invite'])
def invite_friends(message):
    # Placeholder для логики приглашения друзей и начисления токенов
    bot.reply_to(message, "Invite your friends to join us! https://t.me/blackcat_community")

bot.polling(none_stop=True)
