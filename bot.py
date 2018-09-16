import logging
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

import ephem

# Импортируем нужные компоненты
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime, date, time

#Настройки прокси
PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}



#Вывести созвездие выбранной планеты
def get_planet(bot, update):
    planet_name = update.message.text.replace('/planet ','')
    planets = ['Mercury', 'Venus','Earth','Mars','Jupiter','Saturn','Uranus','Neptune']

    if planet_name in planets:
        Planet = getattr(ephem, planet_name)
        cur_date = datetime.now().date()
        now_planet = Planet(cur_date)
        constellation = ephem.constellation(now_planet)
        update.message.reply_text(constellation)

    else:
        update.message.reply_text('Попробуйте ещё раз (на англиском)')



#калькулятор 
def calculation (bot, update):
    expression = update.message.text 
    expression = expression[13:]
    expression = ''.join(expression.split())
#    update.message.reply_text(expression)
   
    if '=' in expression:
        expression = expression[:-1]

        if '+' in expression:
            expression = expression.split('+') 
            ans = int(expression[0]) + int(expression[1])
            update.message.reply_text(ans)
        elif '-' in expression:
            expression = expression.split('-')
            ans = int(expression[0]) - int(expression[1])
            update.message.reply_text(ans)
        elif '*' in expression:
            expression = expression.split('*')
            ans = int(expression[0]) * int(expression[1])
            update.message.reply_text(ans)
        elif '/' in expression:
            try:
                expression = expression.split('/')
                ans = int(expression[0]) / int(expression[1])
                update.message.reply_text(ans)   
            except ZeroDivisionError:
                update.message.reply_text('На ноль делить нельзя!')

    else:
        update.message.reply_text('Не написали равно')




#    x = int(expression[0])
#    y = int(expression[2])
#    z = expression[1]
#    r = expression[3]

#    if r == '=': 

#        if z== '+':
#            ans = x + y
#            update.message.reply_text(ans)
#        elif z== '-':
#            ans = x - y
#            update.message.reply_text(ans)
#        elif z== '*':
#            ans = x * y
#            update.message.reply_text(ans)
#        elif z== '/':
#            ans = x / y 
#            update.message.reply_text(ans)
#    else:
#        update.message.reply_text('Не написали равно')



#Посчитать количество слов во фразе
def word_count (bot, update):
    word = update.message.text 
    #word_list = word.split(' ')
   # del word_list[0]
   # word_string = ' '.join(word_list)
   # word.find(str, ['"'])
   # count = word.find ('"')
    if word.count('"') > 1:
        phrase = word[word.find ('"') +1:word.rfind ('"')-1] 
        count = len(phrase.split(' '))
        if count != 0 :
            update.message.reply_text(count)
        else:
            update.message.reply_text('Ничего не написали')
    else:
         update.message.reply_text('Фраза должна быть в кавычках')


#вызываться, когда пользователь в чате напишет /start вручную или подключится к боту в первый раз
def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)

#Функция ответа
def talk_to_me(bot, update):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)

#Функция, которая создается с платформой телеграм, тело бота
def main():

    mybot = Updater ('key', request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler("planet", get_planet))
    dp.add_handler(CommandHandler("wordcount", word_count))
    dp.add_handler(CommandHandler("calculation", calculation))


    mybot.start_polling()
    mybot.idle()

#Вызываем бота
main()
