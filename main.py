from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import numpy as np
import cv2
import math
import pandas as pd
import env
import json
from glcm import glcm

df = pd.read_excel("extraction.xlsx")

col = 23

x = np.array(df.iloc[:, 0:col])
y = np.array(df['Class'])

allCommand = ("\n/start untuk memulai bot" +
              "\n/help untuk melihat command yang ada" +
              "\n/kelembapantanah untuk mengecek kelembapan tanah" +
              "\n/suhuruangan untuk mengecek suhu ruangan" +
              "\n/kelembapanruangan untuk mengecek kelembapan ruangan" +
              "\n/indexpanas untuk mengecek index panas ruangan" +
              "\n/statuspenyiraman untuk mengecek apakah penyiraman sedang berlangsung" +
              "\n/ceksemua untuk mengecek semua sensor" +
              "\nkirim gambar untuk mendeteksi kandungan unsur hara"+
              "\n(gambar yang dikirim background harus memiliki background putih dan memilikin pencahayaan yang cukup)"+
              "\n\n**Peringatan : Saat pompa sedang menyiram, nilai sensor yang ditampilkan merupakan nilai saat pompa dinyalakan**")


def croppingImage(path):
    # Read image
    img = cv2.imread(path)

    # threshold on white
    # Define lower and uppper limits
    lower = np.array([120, 120, 120])
    upper = np.array([255, 255, 255])

    # Create mask to only select black
    thresh = cv2.inRange(img, lower, upper)

    # apply morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # invert morp image
    mask = 255 - morph

    # apply mask to image
    result = cv2.bitwise_and(img, img, mask=mask)

    cv2.imwrite(path, result)


def imgExtraction(path):
    img = cv2.imread(path)
    hsvImg = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    hue = hsvImg[:, :, 0].mean()
    saturation = hsvImg[:, :, 1].mean()
    value = hsvImg[:, :, 2].mean()
    [g0, g45, g90, g135] = glcm(img)
    return [hue, saturation, value, g0['asm'], g45['asm'], g90['asm'], g135['asm'], g0['kontras'],
            g45['kontras'], g90['kontras'], g135['kontras'], g0['idm'], g45['idm'], g90['idm'],
            g135['idm'], g0['entropi'], g45['entropi'], g90['entropi'], g135['entropi'], g0['korelasi'],
            g45['korelasi'], g90['korelasi'], g135['korelasi']]


def predictKNN(k, attributes):
    ed = []
    res = 0
    for v in x:
        for i in range(col):
            res += ((v[i]-attributes[i])**2)
        ed.append(math.sqrt(res))
        res = 0
    sortedK = [ed for y, ed in sorted(zip(ed, y))]
    return max(set(sortedK[:k]), key=sortedK[:k].count)


def soilMoisture(update, context):
    with open('store.json') as file:
        data = json.load(file)
    update.message.reply_text(
        "kelembapan tanah : "+str(data["kelembapan tanah"])+"%")


def roomTemperature(update, context):
    with open('store.json') as file:
        data = json.load(file)
    update.message.reply_text("suhu ruangan : "+str(data["suhu ruangan"])+"°C")


def roomMoisture(update, context):
    with open('store.json') as file:
        data = json.load(file)
    update.message.reply_text(
        "kelembapan ruangan : "+str(data["kelembapan ruangan"])+"%")


def heatIndex(update, context):
    with open('store.json') as file:
        data = json.load(file)
    update.message.reply_text(
        "index panas ruangan : "+str(data["index panas"])+"°C")


def wateringStatus(update, context):
    with open('store.json') as file:
        data = json.load(file)
    update.message.reply_text(
        "pompa sedang " + ("" if data["siram"] else "tidak ") + "menyiram")


def allStatus(update, context):
    with open('store.json') as file:
        data = json.load(file)
    update.message.reply_text("kelembapan tanah : "+str(data["kelembapan tanah"])+"%" +
                              "\nsuhu ruangan : "+str(data["suhu ruangan"])+"°C" +
                              "\nkelembapan ruangan : "+str(data["kelembapan ruangan"])+"%" +
                              "\nindex panas ruangan : " +
                              str(data["index panas"])+"°C"
                              "\npompa sedang " + ("" if data["siram"] else "tidak ") + "menyiram")

# /start


def start(update, context):
    update.message.reply_text(
        "Selamat Datang \nSilahkan gunakan command di bawah : " + allCommand)


# /help
def help(update, context):
    update.message.reply_text("command yang tersedia adalah : " + allCommand)

# for handle a message


def handleMessage(update, context):
    update.message.reply_text(
        "Silahkan gunakan command di bawah : " + allCommand)


def handleImage(update, context):
    update.message.reply_text("Gambar sedang diproses...")
    # download gambar
    file = context.bot.getFile(file_id=update.message.photo[-1].file_id)
    file.download('image.jpeg')

    # croping
    croppingImage('image.jpeg')

    # ekstraksi gambar
    img = imgExtraction('image.jpeg')

    # knn
    hasil = predictKNN(3, img)

    # send result
    update.message.reply_text("buah "+hasil)

# for error


def error(update, context):
    update.message.reply_text(
        'Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(env.TOKEN, use_context=True)

    dp = updater.dispatcher

    # for command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("kelembapantanah", soilMoisture))
    dp.add_handler(CommandHandler("suhuruangan", roomTemperature))
    dp.add_handler(CommandHandler("kelembapanruangan", roomMoisture))
    dp.add_handler(CommandHandler("indexpanas", heatIndex))
    dp.add_handler(CommandHandler("statuspenyiraman", wateringStatus))
    dp.add_handler(CommandHandler("ceksemua", allStatus))

    # for message
    dp.add_handler(MessageHandler(Filters.text, handleMessage))
    # for image
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
