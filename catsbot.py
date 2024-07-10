import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import requests

TOKEN = '7497254218:AAE2YfsgK1Ir0kJ0N4KwlSDmNjVzajxa5YQ'
bot = telebot.TeleBot(TOKEN)

def calculate_cats(is_premium, account_age_years):
    base_tokens = 5000 if is_premium else 2500
    if account_age_years < 1:
        age_tokens = 1000
    elif account_age_years < 2:
        age_tokens = 2000
    else:
        age_tokens = 3000 + (account_age_years - 2) * 1000
    return base_tokens + age_tokens

def get_user_registration_date(user_id):
    url = f'https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={user_id}&user_id={user_id}'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['ok']:
            user = data['result']['user']
            if 'joined_date' in user:
                timestamp = user['joined_date']
                registration_date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                return registration_date
    except Exception as e:
        print(f"Error getting registration date: {e}")
    
    return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.username or message.from_user.first_name
    is_premium = getattr(message.from_user, 'is_premium', False)
    
    user_id = message.from_user.id
    registration_date = get_user_registration_date(user_id)
    
    if registration_date:
        account_creation_date = datetime.strptime(registration_date, '%Y-%m-%d %H:%M:%S')
        account_age_years = (datetime.now() - account_creation_date).days // 365
    else:
        account_age_years = 0
    
    cats_tokens = calculate_cats(is_premium, account_age_years)
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Let's go", web_app=WebAppInfo(url='https://anbessaa.github.io/catsbot/')))
    
    welcome_message = f"Hello, {username}!\nYou have {cats_tokens} CATS tokens.\n"
    welcome_message += "How cool is your Telegram profile? Check your rating and receive rewards."
    
    bot.reply_to(message, welcome_message, reply_markup=markup)

@bot.message_handler(commands=['invite'])
def invite_friends(message):
    is_premium = getattr(message.from_user, 'is_premium', False)
    bonus_tokens = 4000 if is_premium else 2000
    bot.reply_to(message, f"Invite your friends to join us! https://t.me/blackcat_community\nYou earned {bonus_tokens} CATS tokens!")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "This bot can do amazing things! Just explore.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
