
import sqlite3
import telebot
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, Updater, CallbackContext

def start(update: Updater, context: CallbackContext):
    update.message.reply_text('Привет, ты cтудент?')
    return 1

def search_nick_in_db(nick):
    try:
        sqlite_connection = sqlite3.connect('chinook.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = "SELECT * from employees WHERE EmployeeId=" + nick
        cursor.execute(sqlite_select_query)
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
    if answer.lower() == 'да' or 'yes' :  # заменить на кнопку зайти в админку или добавлять гостя
        update.message.reply_text('напиши ник')
        return 2
    else:
        update.message.reply_text('неправильно!!')
        return ConversationHandler.END

def take_fio_liable(update: Updater, context: CallbackContext):
    #сначала тут поиск по ид потом уже спрашиваем ник
    answer = update.message.text
    if search_nick_in_db(answer) == 1:
        return 3
    else:
        return ConversationHandler.END
    # answer = update.message.text
    # splitMessage = answer.split()
    # surname = splitMessage[0]
    # name = splitMessage[1]
    # patronymic = splitMessage[2]
    # if answer in database // здесь поиск по базе данных
    # return 3
    # else:
        # update.message.reply_text('мда')
    # return ConversationHandler.END

def nick_in_db(update: Updater, context: CallbackContext):
    print('im here')
    update.message.reply_text('твой ник есть в бд')
    return ConversationHandler.END

def stop(bot, update):
    update.message.reply_text("Жаль.")
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
    1: [MessageHandler(Filters.text, pass_or_no_pass)],
    2: [MessageHandler(Filters.text, take_fio_liable)],
    3: [MessageHandler(Filters.text, nick_in_db)]
    },
    fallbacks=[CommandHandler('stop', stop)]
)

updater = Updater('5770334169:AAF4yKlAOnppiB5RJKx2gthxe-49icmWKoI')
dp = updater.dispatcher

dp.add_handler(conv_handler)
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('stop', stop))

updater.start_polling()
updater.idle()