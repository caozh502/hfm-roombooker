import telegram

class bot(object):
    def __init__(self):
        self.bot = telegram.Bot(token='5362557302:AAFm5AapulWqsZd1iAYo8yol-OgNF34qxnw')
        # print (bot.get_me())
        # info = bot.get_webhook_info()
        # print (info)

    def sendMsg(self,text):
        self.bot.send_message(chat_id='@roombookertest', text=str(text))
        print (text)
        

# if __name__ == '__main__':
#     tele = bot()
#     tele.sendMsg("123")

