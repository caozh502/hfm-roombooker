##### Google Colab #####
#@title 步骤2：输入参数→点击运行
mode = 2 #@param ["1", "2"] {type:"raw"}
start_time = "20:30" #@param {type:"string"}
end_time = "22:30" #@param {type:"string"}
room_number = 0 #@param {type:"integer"}
date = "0" #@param {type:"string"}
#################

from operator import imod
from typing import Counter
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import datetime
import pytz
import telebot
import http.client
from telegram.vendor.ptb_urllib3.urllib3.exceptions import ProtocolError
from telegram.error import NetworkError

from roombooker import booker, time_cmp, getNearestMinBack

utc=pytz.UTC
timezone = pytz.timezone("Europe/Berlin")
localtime = datetime.datetime.now(timezone)

def mode_1(roombooker, bot, st, et):
    while True:
        try:
            st_aft30 = st_form+datetime.timedelta(minutes=30)
            st_form = datetime.datetime.strptime(st, "%H:%M")
            et_form = datetime.datetime.strptime(et, "%H:%M")
            # refresh
            localtime = datetime.datetime.now(timezone) 
            ed_tmp = getNearestMinBack(localtime.strftime("%H:%M"))

            roombooker.login()

            # current time > end time
            if time_cmp(localtime,et_form)>0:
                bot.sendMsg("[Situtation] current time > end time")
                if roombooker.roomNum ==0:
                    result = roombooker.find_Termin_EG() or roombooker.find_Termin_OG()
                else:
                    result = roombooker.find_Termin_EG() if int(roombooker.roomNum) in range(101,116) else roombooker.find_Termin_OG() 
                if result:
                    bot.sendMsg("room booked in " + roombooker.resRoomNum + " from " + roombooker.stTime + " to "+ roombooker.edTime)
                else:
                    bot.sendMsg("Cannot find empty room at moment")
            #  (start time +30) < current time < end time
            else:
                if time_cmp(localtime,et_form)<0 and time_cmp(localtime,st_aft30)>0:
                    bot.sendMsg("[Situtation] (start time +30) < current time < end time")
                    while (True):
                        # Temporary use of the end time (because the real end time has not yet arrived,so cannot be used as a valid parameter for find_Termin)
                        roombooker.edTime = ed_tmp.strftime("%H:%M")
                        roombooker.edTime_fm = ed_tmp
                        
                        # try once search
                        bot.sendMsg("[Searching] between "+ st_form.strftime("%H:%M")+" to "+ed_tmp.strftime("%H:%M")+" ...")
                        for i in range(1,3):
                            print ("======== Attempted search time: "+ str(i) +" ========")
                            if roombooker.roomNum==0:
                                result = roombooker.find_Termin_EG() or roombooker.find_Termin_OG()
                            else:
                                result = roombooker.find_Termin_EG() if int(roombooker.roomNum) in range(101,116) else roombooker.find_Termin_OG()
                            if result:
                                break
                        if result:
                            bot.sendMsg("room booked in " + roombooker.resRoomNum + " from " + roombooker.stTime + " to "+ roombooker.edTime)
                            roombooker.edTime = et
                            roombooker.edTime_fm = et_form
                            result_ex = roombooker.extension_time()
                            if result_ex:    
                                break
                        else:
                            bot.sendMsg("[" + localtime.strftime("%H:%M:%S")+"]"+" Cannot find empty room at moment, try again in 15 min later...")
                            # refresh time: all times + 15 min
                            st_form = st_form + datetime.timedelta(minutes=15)
                            et_form = (et_form + datetime.timedelta(minutes=15)) if et_form.strftime("%H:%M")!="23:45" else datetime.datetime.strptime("23:45","%H:%M")
                            st_aft30 = st_form + datetime.timedelta(minutes=30)
                            ed_tmp = ed_tmp + datetime.timedelta(minutes=15) if ed_tmp.strftime("%H:%M")!="23:45" else datetime.datetime.strptime("23:45","%H:%M")
                            st = st_form.strftime("%H:%M")
                            et = et_form.strftime("%H:%M")

                            # deliver the data in roombook Object
                            roombooker.stTime = st
                            roombooker.stTime_fm = st_form

                            print ("refresh the start time and end time: "+ st_form.strftime("%H:%M")+" to "+et_form.strftime("%H:%M"))
                            if (time_cmp(et_form,st_form)<1600): # start time=23:30(2330xx), end time=23:45(2345xx)
                                bot.sendMsg("Cannot find any room today, please try in another day :(")
                                break

                            localtime = datetime.datetime.now(timezone)
                            while (time_cmp(localtime,ed_tmp)<0):
                                print ("[" + localtime.strftime("%H:%M:%S")+"]"+" Waiting for the next 15 minutes")
                                time.sleep(13)
                                localtime = datetime.datetime.now(timezone) # refresh
            break
        except (http.client.RemoteDisconnected, WebDriverException, ProtocolError, NetworkError) as e:
                time.sleep(5)
                if roombooker.counter < 10:
                    print("Internet disconneted, retrying " + str(roombooker.counter+1) +" time")
                    roombooker.counter+=1
                else:
                    print("[END] lost connect")
                    break

def mode_2(roombooker):
    while True:
        try:
            roombooker.login()
            roombooker.extension_time()
            break
        except (http.client.RemoteDisconnected, WebDriverException, ProtocolError, NetworkError) as e:
            time.sleep(5)
            if roombooker.counter < 10:
                print("Internet disconneted, retrying " + str(roombooker.counter+1) +" time")
                roombooker.counter+=1
            else:
                print("[END] lost connect")
                break
        

if __name__ == '__main__':
    # ignore some errors
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])

    localPlus = localtime+datetime.timedelta(days=7)
    lct_str= str(localtime.day)+'.'+str(localtime.month)+'.'+str(localtime.year)
    localtime_fm=datetime.datetime.strptime(lct_str,'%d.%m.%Y')
    ## headless, no window
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")

    telebot = telebot.bot()

    if mode==1:

        # Input
        st = start_time
        et = end_time
        date=date+'.'+str(localtime.year) if int(date)!=0 else str(localPlus.day)+'.'+str(localPlus.month)+'.'+str(localPlus.year)
        # format time
        st_form = datetime.datetime.strptime(st, "%H:%M")
        st_aft30 = st_form+datetime.timedelta(minutes=30)
        et_form = datetime.datetime.strptime(et, "%H:%M")
        ed_tmp = getNearestMinBack(localtime.strftime("%H:%M"))
        date_form = datetime.datetime.strptime(date,'%d.%m.%Y')

        # Pass parameters to the booker class
        data = ['https://hfm-karlsruhe.asimut.net/public/login.php',  '13200',  'ZXY200238zxy.',options, st,et,room_number,date]
        roombooker = booker(data)
        
        # Error input
        if date_form>(localtime_fm+datetime.timedelta(days=7)) or date_form<localtime_fm :
            print ('Your input date is overrange, please try to enter again.')
            exit()

        #  current time < (start time +30) and date = today+7
        mark_telebot = 1
        while time_cmp(localtime,st_aft30)<0 and date_form==(localtime_fm+datetime.timedelta(days=7)):
            if (mark_telebot==True):
                telebot.sendMsg("[Situtation] current time < (start time +30)")
                telebot.sendMsg("[" + localtime.strftime("%H:%M:%S")+"]"+" waiting until reservation is possible")
                mark_telebot = 0
            print ("[" + localtime.strftime("%H:%M:%S")+"]"+" waiting until reservation is possible")
            time.sleep(13)

            # refresh
            localtime = datetime.datetime.now(timezone) 
            ed_tmp = getNearestMinBack(localtime.strftime("%H:%M"))

        mode_1(roombooker, telebot, st, et)

    elif mode ==2:

        # Input
        date=date+'.'+str(localtime.year) if date!='0' else str(localPlus.day)+'.'+str(localPlus.month)+'.'+str(localPlus.year)
        st = start_time
        et = end_time
        num_room= room_number # default
        
        data = ['https://hfm-karlsruhe.asimut.net/public/login.php',  '13200',  'ZXY200238zxy.',options, st, et, num_room, date]
        roombooker = booker(data)

        mode_2(roombooker)

    # exit browser
    roombooker.driver.quit()


            
