# from tkinter.messagebox import NO
# from venv import create

import telebot
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, Updater, CallbackContext, CallbackQueryHandler
import data_base as db
from pathlib import Path

#from telebot import types

database = "db.db"
path = Path(database)
conn = None
if (path.is_file()):
    conn = db.create_connection(database)
else:
    conn = db.create_data_base(database)

#bot = telebot.TeleBot('939129359:AAF5qJUUmuityqGijDTqOPGm7uLkOGos1us')
def start(update: Updater, context: CallbackContext):
    res = db.search_nick_by_usrname(conn, update.message.chat.username)
    if len(res) == 0: # если уже есть в базе его username
        update.message.reply_text('напиши ник я добавлю тебя в базу и запомню')
        return 4
    else:
        update.message.reply_text('Назови того кого хочешь позвать! (ФИО полностью)')
        return 3

def insert_id(update: Updater, context: CallbackContext): # юзера не было в базе
    nick = update.message.text
    if db.search_nick_in_db(conn, nick) != 0:
        db.ubdate_username(conn, nick, update.message.chat.username)
        update.message.reply_text('Назови того кого хочешь позвать!')
        return 3
    else:
        update.message.reply_text('К сожалению я не знаю тебя и ты не можешь никого пригласить :с')
        return ConversationHandler.END

def take_fio_liable(update: Updater, context: CallbackContext):
    nick = update.message.text
    if db.search_nick_in_db(conn, nick) == 1:
        update.message.reply_text('Назови того кого хочешь позвать! (ФИО полностью)')
        return 3
    else:
        update.message.reply_text('К сожалению я не знаю тебя и ты не можешь никого пригласить :с')
        return ConversationHandler.END

def nick_in_db(update: Updater, context: CallbackContext):
    guest_fio = update.message.text
    user_fio = db.search_nick_by_usrname(conn, update.message.chat.username)[0][1]
    db.insert_pass(conn, guest_fio, user_fio)
    #return 7
    return ConversationHandler.END

def set_visit_time(time, nik):
    sqliteConnection = sqlite3.connect('db.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sql_update_query = """Update pass set time_of_action_pass = ? where nik = ?"""

    count = cursor.execute(sql_update_query, (time, nik))
    sqliteConnection.commit()
    print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
    cursor.close()

days = ['22.08(Пн)', '23.08(Вт)', '24.08(Ср)', '25.08(Чт)', '26.08(Пт)', '27.08(Сб)', '28.08(Вс)']
times = ['10.00-12.00', '12.00-14.00', '14.00-16.00', '16.00-18.00']

def butt_day(update: Updater, context: CallbackContext):
    answer = update.message.text
    markup_inline = types.InlineKeyboardMarkup()
    item_1 = types.InlineKeyboardButton(text = days[0], callback_data = '1')
    item_2 = types.InlineKeyboardButton(text = days[1], callback_data = '2')
    item_3 = types.InlineKeyboardButton(text = days[2], callback_data = '3')
    item_4 = types.InlineKeyboardButton(text = days[3], callback_data = '4')
    item_5 = types.InlineKeyboardButton(text = days[4], callback_data = '5')
    item_6 = types.InlineKeyboardButton(text = days[5], callback_data = '6')
    item_7 = types.InlineKeyboardButton(text = days[6], callback_data = '7')
    markup_inline.add(item_1, item_2, item_3, item_4, item_5, item_6, item_7)
    bot.send_message(update.message.chat.id, 'Выбери день посещения', reply_markup = markup_inline)
    return 8

def butt_time(update: Updater, context: CallbackContext):
    markup_inline = types.InlineKeyboardMarkup()
    item_10 = types.InlineKeyboardButton(text = times[0], callback_data = '10')
    item_12 = types.InlineKeyboardButton(text = times[1], callback_data = '12')
    item_14 = types.InlineKeyboardButton(text = times[2], callback_data = '14')
    item_16 = types.InlineKeyboardButton(text = times[3], callback_data = '16')
    markup_inline.add(item_10, item_12, item_14, item_16)
    bot.send_message(update.message.chat.id, 'Выбери время посещения', reply_markup = markup_inline)
    return 8

def answer(bot, update):
    callback_data = bot.callback_query.data
    bot.callback_query.answer()
    if callback_data == '1':
        day = days[0]
        return 9
    if callback_data == '2':
        day = days[1]
        return 9
    if callback_data == '3':
        day = days[2]
        return 9
    if callback_data == '4':
        day = days[3]
        return 9
    if callback_data == '5':
        day = days[4]
        return 9
    if callback_data == '6':
        day = days[5]
        return 9
    if callback_data == '7':
        day = days[6]
        return 9
    if callback_data == '10':
        time = times[0]
        take_your_time()
    if callback_data == '12':
        time = times[1]
        take_your_time()
    if callback_data == '14':
        time = times[2]
        take_your_time()
    if callback_data == '16':
        time = times[3]
        take_your_time()

def take_your_time():
    day = '22.08' # убрать
    time =  '10.00-12.00' # убрать
    nik = 'johniety' # убрать
    set_visit_time(day + ' ' + time, nik) # сделать day time из answer и nik глобальными (у меня не получилось) и дергать оттуда 

def stop(update: Updater, context: CallbackContext):
    update.message.reply_text("Жаль.")
    conn.close()
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
    # 1: [MessageHandler(Filters.text, pass_or_no_pass)],
    2: [MessageHandler(Filters.text, take_fio_liable)],
    3: [MessageHandler(Filters.text, nick_in_db)],
    4: [MessageHandler(Filters.text, insert_id)],
    7: [MessageHandler(None, butt_day)],
    8: [CallbackQueryHandler(answer)],
    9: [MessageHandler(None, butt_time)]
    },
    fallbacks=[CommandHandler('stop', stop)]
)

updater = Updater('5770334169:AAF4yKlAOnppiB5RJKx2gthxe-49icmWKoI')
disp = updater.dispatcher

disp.add_handler(conv_handler)
disp.add_handler(CommandHandler('start', start))
disp.add_handler(CommandHandler('stop', stop))
updater.start_polling()
updater.idle()