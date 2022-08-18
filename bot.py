
import sqlite3
import telebot
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, Updater, CallbackContext

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

def search_nick_by_id(id):
    try:
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = "SELECT * from users WHERE userid=?"
        cursor.execute(sqlite_select_query, (id,))
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


def pass_or_no_pass(update: Updater, context: CallbackContext):
    answer = update.message.text
    if answer.lower() == 'да' :  # заменить на кнопку зайти в админку или добавлять гостя
        if search_nick_by_id(update.message.from_user.id) == 0:
            update.message.reply_text('напиши ник я добавлю тебя в базу и запомню')
            return 4
        else:
            return ConversationHandler.END
    else:
        update.message.reply_text('неправильно!!')
        return ConversationHandler.END

def insert_id(update: Updater, context: CallbackContext):
    nick = update.message.text
    print("inserting") # ВСТАВКУ В БД ДОБАВИТЬ
    if search_nick_in_db(nick) == 1:
        update.message.reply_text('Назови того кого хочешь позвать!')
        return 3

def take_fio_liable(update: Updater, context: CallbackContext):
    nick = update.message.text
    if search_nick_in_db(nick) == 1:
        update.message.reply_text('Назови того кого хочешь позвать!')
        return 3
    else:
        update.message.reply_text('К сожалению я не знаю тебя и ты не можешь никого пригласить :с')
        return ConversationHandler.END

def nick_in_db(update: Updater, context: CallbackContext):
    guest_fio = update.message.text
    update.message.reply_text("Ну хорошо а теперь выбери время!")
    update.message.reply_text("тут интервалы")
    return 5

def take_your_time(update: Updater, context: CallbackContext):
    
    return ConversationHandler.END

def stop(bot, update):
    update.message.reply_text("Жаль.")
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
    1: [MessageHandler(Filters.text, pass_or_no_pass)],
    2: [MessageHandler(Filters.text, take_fio_liable)],
    3: [MessageHandler(Filters.text, nick_in_db)],
    4: [MessageHandler(Filters.text, insert_id)],
    5: [MessageHandler(Filters.text, take_your_time)]
    },
    fallbacks=[CommandHandler('stop', stop)]
)

updater = Updater('939129359:AAF5qJUUmuityqGijDTqOPGm7uLkOGos1us')
dp = updater.dispatcher

dp.add_handler(conv_handler)
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('stop', stop))

updater.start_polling()
updater.idle()