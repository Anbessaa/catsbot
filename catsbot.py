import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from datetime import datetime
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest

TOKEN = '7497254218:AAE2YfsgK1Ir0kJ0N4KwlSDmNjVzajxa5YQ'
API_ID = '28653734'
API_HASH = 'f5099d7504bcbb7f5cd7f949e60462a0'

bot = telebot.TeleBot(TOKEN)
client = TelegramClient('session', API_ID, API_HASH)

async def get_user_registration_date(user_id):
    await client.start()
    try:
        full_user = await client(GetFullUserRequest(user_id))
        # Используем первое сообщение пользователя как приближение даты регистрации
        messages = await client.get_messages(user_id, limit=1, reverse=True)
        if messages:
            return messages[0].date
        return None
    finally:
        await client.disconnect()

def calculate_cats(is_premium, account_age_years):
    base_tokens = 5000 if is_premium else 2500
    if account_age_years < 1:
        age_tokens = 1000
    elif account_age_years < 2:
        age_tokens = 2000
    else:
        age_tokens = 3000 + int((account_age_years - 2) * 1000)
    return base_tokens + age_tokens

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    is_premium = getattr(message.from_user, 'is_premium', False)
    
    # Получаем дату регистрации
    registration_date = asyncio.run(get_user_registration_date(user_id))
    if registration_date:
        account_age_years = (datetime.now(registration_date.tzinfo) - registration_date).days / 365.25
    else:
        account_age_years = 0
    
    cats_tokens = calculate_cats(is_premium, account_age_years)
    
    # Отправка изображения кота
    with open('cat_image.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Let's go", web_app=WebAppInfo(url='https://anbessaa.github.io/catsbot/')))
    
    welcome_message = f"Hello, {username}!\n"
    welcome_message += "How cool is your Telegram profile? Check your rating and receive rewards."
    
    bot.reply_to(message, welcome_message, reply_markup=markup)
    
    # Отправляем данные в веб-приложение
    bot.answer_web_app_query(message.web_app_query_id, {
        'type': 'article',
        'id': '1',
        'title': 'User Data',
        'input_message_content': {
            'message_text': f'account_age_years:{account_age_years:.2f},is_premium:{is_premium},cats_tokens:{cats_tokens}'
        }
    })

if __name__ == "__main__":
    bot.polling(none_stop=True)
