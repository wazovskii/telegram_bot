
import sqlite3
import telebot
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, Updater, CallbackContext, CallbackQueryHandler
from telebot import types

bot = telebot.TeleBot('939129359:AAF5qJUUmuityqGijDTqOPGm7uLkOGos1us')
def start(update: Updater, context: CallbackContext):
    update.message.reply_text('Привет, ты cтудент?')
    return 1

def search_nick_in_db(nick):
    result = 0
    try:
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        sqlite_select_query = "SELECT * from users WHERE nik=?"
        cursor.execute(sqlite_select_query, (nick,))
        records = cursor.fetchall()
        result = len(records)
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    return result

def search_nick_by_id(usern):
    try:
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = "SELECT * from users WHERE username=?"
        cursor.execute(sqlite_select_query, (usern,))
        records = cursor.fetchall()
        result = records
        # for row in records:
        #     print(row)
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    return result


def pass_or_no_pass(update: Updater, context: CallbackContext):
    answer = update.message.text
    if answer.lower() == 'yes' :  # заменить на кнопку зайти в админку или добавлять гостя
        if len(search_nick_by_id(update.message.chat.username)) == 0:
            update.message.reply_text('напиши ник я добавлю тебя в базу и запомню')
            return 4
        else:
            update.message.reply_text('Назови того кого хочешь позвать!')
            return 3
    else:
        update.message.reply_text('неправильно!!')
        return ConversationHandler.END

def insert_in_db(nick, usern):
    sqliteConnection = sqlite3.connect('db.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sql_update_query = """Update users set username = ?  where nik = ?"""

    count = cursor.execute(sql_update_query, (usern, nick))
    sqliteConnection.commit()
    print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
    cursor.close()

def insert_id(update: Updater, context: CallbackContext):
    nick = update.message.text
    insert_in_db(nick, update.message.chat.username)
    if search_nick_in_db(nick) == 1:
        update.message.reply_text('Назови того кого хочешь позвать!')
        return 3

def take_fio_liable(update: Updater, context: CallbackContext):
    nick = update.message.text
    if search_nick_in_db(nick) == 1:
        update.message.reply_text('Назови того кого хочешь позвать! (ФИО полностью)')
        return 3
    else:
        update.message.reply_text('К сожалению я не знаю тебя и ты не можешь никого пригласить :с')
        return ConversationHandler.END

def take_fio_liable_known(update: Updater, context: CallbackContext):
    
    return 3

def insert_pass(guest_fio, user_fio, nick):
    sqliteConnection = sqlite3.connect('db.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sql_update_query = "INSERT or IGNORE INTO pass (nik, FIO_guest, FIO_user, time_of_action_pass, validity, status_pass) VALUES (?, ?, ?, ?, ?, ?)"

    count = cursor.execute(sql_update_query, (nick, guest_fio, user_fio, None, None, None))
    sqliteConnection.commit()
    print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
    cursor.close()


def nick_in_db(update: Updater, context: CallbackContext):
    guest_fio = update.message.text
    sech = search_nick_by_id(update.message.chat.username)
    user_fio = sech[0][3]
    nick = search_nick_by_id(update.message.chat.username)[0][2]
    insert_pass(guest_fio, user_fio, nick)
    butt_day(update)
    return 5

def set_visit_time(time, FIO_guest):
    sqliteConnection = sqlite3.connect('db.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sql_update_query = """Update users set time_of_action_pass = ?  where FIO_guest = ?"""

    count = cursor.execute(sql_update_query, (time, FIO_guest))
    sqliteConnection.commit()
    print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
    cursor.close()

days = ['22.08(Пн)', '23.08(Вт)', '24.08(Ср)', '25.08(Чт)', '26.08(Пт)', '27.08(Сб)', '28.08(Вс)']
times = ['10.00-12.00', '12.00-14.00', '14.00-16.00', '16.00-18.00']

def butt_day(update: Updater, context: CallbackContext):
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

def butt_time(update):
    markup_inline = types.InlineKeyboardMarkup()
    item_10 = types.InlineKeyboardButton(text = times[0], callback_data = '10')
    item_12 = types.InlineKeyboardButton(text = times[1], callback_data = '12')
    item_14 = types.InlineKeyboardButton(text = times[2], callback_data = '14')
    item_16 = types.InlineKeyboardButton(text = times[3], callback_data = '16')
    markup_inline.add(item_10, item_12, item_14, item_16)
    bot.send_message(update.message.chat.id, 'Выбери время посещения', reply_markup = markup_inline)
    # print('ddd')


def answer(update, context):
    callback_data = update.callback_query.data
    # update.callback_query.answer() 
    if callback_data == '1':
        day = days[0]
        # print('fuc you')
        return 7
    if callback_data == '2':
        day = days[1]
        return 7
    # if callback_data == '3':
    #     day = days[2]
    #     butt_time(update)
    # if callback_data == '4':
    #     day = days[3]
    #     butt_time(update)
    # if callback_data == '5':
    #     day = days[4]
    #     butt_time(update)
    # if callback_data == '6':
    #     day = days[5]
    #     butt_time(update)
    # if callback_data == '7':
    #     day = days[6]
    #     butt_time(update)

    if callback_data == '10':
        time = times[0]
        return 5
    if callback_data == '12':
        time = times[1]
        return 5
    if callback_data == '14':
        time = times[2]
        return 5
    if callback_data == '16':
        time = times[3]
        return 5

def take_your_time(update: Updater, context: CallbackContext):
    set_visit_time()
    return ConversationHandler.END

def stop(bot, update):
    update.message.reply_text("Жаль.")
    return ConversationHandler.END

def handler_yes_no(update, context):
    update.callback_query.answer() 
    print(callback_data)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
    1: [MessageHandler(Filters.text, pass_or_no_pass)],
    2: [MessageHandler(Filters.text, take_fio_liable)],
    3: [MessageHandler(Filters.text, nick_in_db)],
    4: [MessageHandler(Filters.text, insert_id)],
    5: [MessageHandler(Filters.text, take_your_time)],
    6: [MessageHandler(Filters.text, take_fio_liable_known)],
    7: [MessageHandler(Filters.text, butt_time)]
    },
    fallbacks=[CommandHandler('stop', stop)]
)

updater = Updater('939129359:AAF5qJUUmuityqGijDTqOPGm7uLkOGos1us')
dp = updater.dispatcher

dp.add_handler(conv_handler)
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CallbackQueryHandler(answer, pattern=r'^(1|2|3|4|5|6|7|10|12|14|16)'))
dp.add_handler(CommandHandler('stop', stop))
updater.start_polling()
updater.idle()