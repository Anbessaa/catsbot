from flask import Flask, request, jsonify
from telebot import TeleBot, types
import sqlite3
from datetime import datetime

app = Flask(__name__)
bot = TeleBot('7497254218:AAE2YfsgK1Ir0kJ0N4KwlSDmNjVzajxa5YQN')

# Инициализация базы данных
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (user_id INTEGER PRIMARY KEY, join_date TEXT, is_premium INTEGER, cats_tokens INTEGER)''')
conn.commit()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Let's go", web_app=types.WebAppInfo(url='https://anbessaa.github.io/catsbot/')))
    bot.reply_to(message, "How cool is your Telegram profile? Check your rating and receive rewards.", reply_markup=markup)

@app.route('/webapp', methods=['GET', 'POST'])
def webapp():
    if request.method == 'POST':
        user_data = request.json
        user_id = user_data['id']
        
        # Проверка и обновление данных пользователя
        c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        user = c.fetchone()
        if user is None:
            join_date = datetime.now().strftime("%Y-%m-%d")
            c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (user_id, join_date, 0, 0))
        else:
            join_date = user[1]
        
        # Расчет статуса и токенов
        years_in_telegram = (datetime.now() - datetime.strptime(join_date, "%Y-%m-%d")).days // 365
        is_premium = user_data.get('is_premium', False)
        cats_tokens = calculate_cats_tokens(years_in_telegram, is_premium)
        
        # Обновление данных в базе
        c.execute("UPDATE users SET is_premium=?, cats_tokens=? WHERE user_id=?", (int(is_premium), cats_tokens, user_id))
        conn.commit()
        
        return jsonify({
            'status': 'Premium' if years_in_telegram >= 4 else 'Standard',
            'cats_tokens': cats_tokens
        })
    else:
        return app.send_static_file('index.html')

def calculate_cats_tokens(years, is_premium):
    base_tokens = years * 100
    premium_bonus = 500 if is_premium else 0
    return base_tokens + premium_bonus

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    c.execute("SELECT user_id, cats_tokens FROM users ORDER BY cats_tokens DESC LIMIT 10")
    leaders = c.fetchall()
    return jsonify(leaders)

@app.route('/invite', methods=['POST'])
def invite_friend():
    user_data = request.json
    user_id = user_data['id']
    friend_id = user_data['friend_id']
    
    # Логика начисления бонусов за приглашение
    bonus = 50
    c.execute("UPDATE users SET cats_tokens = cats_tokens + ? WHERE user_id=?", (bonus, user_id))
    conn.commit()
    
    return jsonify({'success': True, 'bonus': bonus})

if __name__ == '__main__':
    app.run(debug=True)
