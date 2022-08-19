import telebot
from aiogram import types
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

token = '5726974119:AAF10aVFmLMSrf1hBX2OA8T1_gSYs9ObMbo'
bot = telebot.TeleBot(token)

bd_1 = ["reynardk"]
bd_2 = {}

def send_pass(nic):  # функция отправки письма с кодом
    try:
        fromaddr = 'syvorov.daniil@gmail.com'  # адрес 
        mypass = 'pezlmttxnbsalypy'            # это я помаялся и сделал пароль для доступа к моему аккаунту из вне, можно сделать для любой почты пусть пока моя
        toaddr =  nic + "@student.21-school.ru"  # из ника делаем почту
        msg = MIMEMultipart()    # генерируем форму письма
        msg['From'] = fromaddr   # от кого
        msg['To'] = toaddr       # кому
        msg['Subject'] = "check code"  # заголовок письма
        code = random.randint(1, 999999)   # герерируем код проверки
        body = "Your test code is " + str(code)  # текс писмьма
        msg.attach(MIMEText(body, 'plain'))      # получаем самое письмо уже для отправки
        server = smtplib.SMTP('smtp.gmail.com: 587')   # стартуем сервер для отправки
        server.starttls()                              # делаем что-то еще)))
        server.login(fromaddr, mypass)                 # регестрируем отправителя
        text = msg.as_string()                         # переводим письмо в нужную форму
        server.sendmail(fromaddr, fromaddr, text)      # отправляем
        server.quit()                                  # завершаем работу сервера
        return code    # вощвращаем код
    except Exception:
        return 0

@bot.message_handler(commands=["start"])  # вызов при команде старт
def start(message, res=False):
    if (message.chat.username in bd_2): # проверям в базе может уже такой бфл зарегестрирован
        bot.send_message(message.chat.id, "Привет " + str(bd_2[message.chat.username])) # приветствуем по нику
    else:     # иначе нужно регестрировать!
        bot.send_message(message.chat.id, "Представься!")
        bot.register_next_step_handler(message, registr) # вызываем другую функцию которая будет ждать сообщения

def registr(message):
    nic = message.text # должен быть введен ник
    if (nic in bd_1):  # проверям в бд есть ли такой пользователь
        code = send_pass(nic)   # высылаем код
        if (code != 0):
            bot.send_message(message.chat.id, "Тебе на почту отправлен код, введи его!")
            bot.register_next_step_handler(message, check_reg, code, nic) # также вызываем другую функцию которая ждетт ввода кода проверки
        else:
            bot.send_message(message.chat.id, "ERROR!")
    else:
        bot.send_message(message.chat.id, "Пользователя с таким ником не существует!")

def check_reg(message, code, nic):
    if (message.text == str(code)): # если код совпадает добавляем в базу данных username этого пользователя
        bd_2[message.chat.username] = nic
        bot.send_message(message.chat.id, "Привет " + nic)
    else:
        bot.send_message(message.chat.id, "ERROR CODE!")

bot.polling(none_stop=True)