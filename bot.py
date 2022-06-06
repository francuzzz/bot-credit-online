import telebot
import sqlite3
import time
from telebot import types

bot = telebot.TeleBot('1415525622:AAEDGEYgmeJzZUoT6UM8tr2yjctUdb3foGA')
city = '';
age = 0;
summa = '';
conn = sqlite3.connect('db/database.db', check_same_thread=False)
cursor = conn.cursor()

def db_table_val(user_id: int, user_name: str, user_surname: str, username: str, city: str, summa: int, age: int):
    cursor.execute('INSERT INTO test (user_id, user_name, user_surname, username, city, summa, age) VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id, user_name, user_surname, username, city, summa, age))
    conn.commit()


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id,  "Салем, " + message.from_user.first_name + "! Я Алина 😉\nВаш персональный кредитный специалист." )
    msg_city = bot.send_message(message.from_user.id, 'Из какого вы города?');
    bot.register_next_step_handler(msg, get_city);


def get_city(message): #получаем город
    global city;
    city = message.text;
    bot.send_message(message.from_user.id, 'Какая сумма Вас интересует?');
    bot.register_next_step_handler(message, get_summa);	

def get_summa(message): #получаем сумму
    global summa;
    try:
        summa = message.text
		
    			
        if not summa.isdigit():
            msg = bot.reply_to(message, 'А это точно число? 🧐\nДавайте попробуем еще раз...')
            bot.register_next_step_handler(msg, get_summa)
            return
    	
    except Exception as e:
        bot.reply_to(message, 'oooops')
    bot.send_message(message.from_user.id, 'Сколько Вам лет?');			
    bot.register_next_step_handler(message, get_age);
    

def get_age(message): #получаем возраст
    try:
        age = message.text
		
    			
        if not age.isdigit():
            msg = bot.reply_to(message, 'А это точно возраст? 🧐\nДавайте попробуем еще раз...')
            bot.register_next_step_handler(msg, get_age)
            return
        if int(age) >= 85:
            bot.reply_to(message, "С уважением отношусь к Вашему возрасту, но получить кредит будет сложно 🧙\nДавайте попробуем еще раз...")
            bot.register_next_step_handler(msg, get_age)
            return           	
    except Exception as e:
        bot.send_message(message.from_user.id, 'Давайте попробуем')
    time.sleep(3);    
    bot.send_message(message.from_user.id, 'Подбираю подходящие предложения')
    time.sleep(3);
    bot.send_message(message.from_user.id, message.from_user.first_name+', нашла компании в г.'+city+ ',\nкоторые готовы одобрить Вам '+str(summa)+ '''тг.\nс любой кредитной историей:
    
✅ Деньги Click ➡️https://bit.ly/3ii7vkt - Без справок, документов и залога. Можно получить наличными, на карту и на счет.
    
✅ Честное слово  ➡️ https://bit.ly/3qg4bum - Новым клиентам до 40 000 тг. Станьте постоянным клиентом, получайте большую сумму + скидки и промокоды
    
✅ Lenily ➡️ https://bit.ly/37vZPZG Возьмите деньги сейчас, а отдайте через год!
    

*Подайте заявку минимум в 3 организации, для  100% результата!*   
    ''');

    # if int(age) <= 17:
    # 		bot.send_message(message.chat.id, "Рано!")
    
    # if int(age) >= 62:
    # 		bot.send_message(message.chat.id, "Поздно!")

    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username


		
    db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username, city=city, summa=summa, age=age)



bot.polling(none_stop=True, interval=0)