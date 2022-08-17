import telebot;
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, Updater, CallbackContext
# bot = telebot.TeleBot('5770334169:AAF4yKlAOnppiB5RJKx2gthxe-49icmWKoI');


def start(update: Updater, context: CallbackContext):
    update.message.reply_text('Привет, дать пропуск?')
    return 1

def pass_or_no_pass(update: Updater, context: CallbackContext):
    answer = update.message.text
    if answer.lower() == 'да':
        update.message.reply_text('напиши свое ФИО')
        return 2
    else:
        update.message.reply_text('мда')
        return ConversationHandler.END

def take_fio_liable(update: Updater, context: CallbackContext):
    answer = update.message.text
    if answer.lower() == 'да':
        update.message.reply_text('напиши свое ФИО')
        return 2
    else:
        update.message.reply_text('мда')
        return ConversationHandler.END

def stop(bot, update):
    update.message.reply_text("Жаль.")
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
    1: [MessageHandler(Filters.text, pass_or_no_pass)],
    2: [MessageHandler(Filters.text, take_fio_liable)]
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