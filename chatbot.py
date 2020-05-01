# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json

updater = Updater(token='1150717031:AAHrSmnaIL8KoPX_PibOYx9KLtl43jgKIWo') # Токен API к Telegram
dispatcher = updater.dispatcher
# Обработка команд

def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Здравствуйте! Я ваш помощник. Спросите у меня, что я могу, и я с радостью вам что-то подскажу')
	
	
def textMessage(bot, update):
    request = apiai.ApiAI('187c0b55f51a426f97d0eeeba3ec2def').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'AI_Helperbot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял! Повторите запрос или обратитесь в поддержку')
# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
