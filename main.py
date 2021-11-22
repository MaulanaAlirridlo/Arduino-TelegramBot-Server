from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import env

# /start
def start(update, context):
    update.message.reply_text('Selamat Datang \nSilahkan gunakan command di bawah : \n/start')


# /help
def help(update, context):
    update.message.reply_text('Help!')

# for handle a message
def handleMessage(update, context):
    update.message.reply_text("Silahkan gunakan command di bawah : \n /start")

# for error
def error(update, context):
    update.message.reply_text('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(env.TOKEN, use_context=True)

    dp = updater.dispatcher

    # for command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # for message
    # dp.add_handler(MessageHandler(Filters.text, handleMessage))

    # if error
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # make bot to stay active
    updater.idle()


if __name__ == '__main__':
    main()