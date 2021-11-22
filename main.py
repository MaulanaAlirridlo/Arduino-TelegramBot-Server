from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import env

# /start
def start(update, context):
    update.message.reply_text("Selamat Datang \nSilahkan gunakan command di bawah : "+
    "\n /start untuk memulai bot"+
    "\n/help untuk melihat command yang ada"+
    "\nkirim gambar untuk mendeteksi kandungan unsur hara")


# /help
def help(update, context):
    update.message.reply_text("command yang tersedia adalah : "+
    "\n /start untuk memulai bot"+
    "\n/help untuk melihat command yang ada"+
    "\nkirim gambar untuk mendeteksi kandungan unsur hara")

def soilMoisture(update, context):
    update.message.reply_text("kelembapan : ")

# for handle a message
def handleMessage(update, context):
    update.message.reply_text("Silahkan gunakan command di bawah : "+
    "\n /start untuk memulai bot"+
    "\n/help untuk melihat command yang ada"+
    "\nkirim gambar untuk mendeteksi kandungan unsur hara")

def handleImage(update, context):
    update.message.reply_text("Gambar sedang diproses...")

# for error
def error(update, context):
    update.message.reply_text('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(env.TOKEN, use_context=True)

    dp = updater.dispatcher

    # for command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("kelembapan", soilMoisture))

    # for message
    dp.add_handler(MessageHandler(Filters.text, handleMessage))
    dp.add_handler(MessageHandler(Filters.photo, handleImage))
    dp.add_handler(MessageHandler(Filters.document.image, handleImage))

    # if error
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # make bot to stay active
    updater.idle()

if __name__ == '__main__':
    main()