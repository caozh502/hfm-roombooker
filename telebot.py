import telegram
bot = telegram.Bot(token='5362557302:AAFm5AapulWqsZd1iAYo8yol-OgNF34qxnw')
# print (bot.get_me())
info = bot.get_webhook_info()
print (info)
bot.send_message(chat_id='@roombookertest', text=str("Hello World"))