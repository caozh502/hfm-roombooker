##### Google Colab #####
#@title 步骤2：输入参数→点击运行
mode = 1 #@param ["1", "2"] {type:"raw"}
start_time = "17:15" #@param {type:"string"}
end_time = "20:15" #@param {type:"string"}
room_number = 0 #@param {type:"integer"}
date = "0" #@param {type:"string"}
#################

# from xmlrpc.client import DateTime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import datetime
from selenium.common.exceptions import NoSuchElementException
import pytz
import telebot

utc=pytz.UTC
timezone = pytz.timezone("Europe/Berlin")
localtime = datetime.datetime.now(timezone)

def time_cmp(first_time, second_time):
    return (int(first_time.strftime("%H%M%S")) - int(second_time.strftime("%H%M%S")))

def getNearestMinBack(t):
    time = datetime.datetime.strptime(t, "%H:%M")
    time= time.replace(minute=(time.minute//15)*15)
    return time

def getNearestMinFor(t):
    time = datetime.datetime.strptime(t, "%H:%M")
    time= time.replace(minute=(time.minute//15+1)*15) if time.minute//15!=3 else time.replace(minute=0,hour=time.hour+1)
    return time

def diffMin(t1,t2):
    t1= datetime.datetime.strptime(t1.strftime("%H:%M"),"%H:%M")
    t2= datetime.datetime.strptime(t2.strftime("%H:%M"),"%H:%M")
    diff = t1 -t2
    return (int(diff.seconds/60))

class booker(object):
    
    def __init__(self,data):
        self.url = data[0]
        self.acc = data[1]
        self.psw = data[2]
        self.opt = data[3]
        self.stTime = data[4]
        self.stTime_fm = datetime.datetime.strptime(data[4], "%H:%M") # format start time
        self.edTime = data[5]
        self.edTime_fm = datetime.datetime.strptime(data[5], "%H:%M") # format end time
        self.roomNum = data[6]
        self.date = data[7] if data[7]!='0' else (localtime+datetime.timedelta(days=7))
        self.date_fm = datetime.datetime.strptime(data[7],'%d.%m.%Y').replace(tzinfo=utc)
        self.resRoomNum = '0'
        self.bot = telebot.bot()
        

    def login(self):   
        print ("[Login]")
        # set chromedriver
        self.driver=webdriver.Chrome(options=self.opt)
        self.driver.maximize_window()  #设置窗口最大化
        self.driver.implicitly_wait(1) #设置等待1秒后打开目标网页

        self.driver.get(self.url)
        account=self.driver.find_element(By.ID,"authenticate-useraccount")
        account.send_keys(self.acc)
        psw=self.driver.find_element(By.ID,'authenticate-password')
        psw.send_keys(self.psw)
        btn_login=self.driver.find_element(By.ID,'loginSubmitButton')
        btn_login.click()
        login_info=self.driver.find_element(By.XPATH,'//*[@id="left-column"]/h1[1]')
        if 'Xinyuan Zhang' in login_info.text:
            print ('successfully login')
        else:
            print ('failed login')
        
    def find_Termin_EG(self):
        print ("[find Termin in EG]")
        delta_date = (localtime+datetime.timedelta(days=7)-self.date_fm).days
        counter_room = 0
        # invalid_room = [75]
        invalid_room = [75]
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        btn_EG=self.driver.find_element(By.XPATH,'//*[@id="left-column"]/h2[1]/a').click()
        # btn_EG.click()
        
        if self.roomNum == 0: # no input of room number
            for i in range (65,80):
                # if (i not in invalid_room): 
                EG_room = self.driver.find_element(By.ID,"chart-row-"+str(i)).find_element(By.CLASS_NAME,"event-location").click()
                    # EG_room.click()
                try:
                    btn_book = self.driver.find_element(By.XPATH,'//*[@id="function-span"]/p['+str(8-delta_date)+']/a').click()
                    # btn_book.click()
                except NoSuchElementException:
                    print ('error: NoSuchElementException')
                    self.driver.back()
                    time.sleep(0.1)
                    continue    
                
                # Enter preset content
                startTime =self.driver.find_element(By.XPATH,'//*[@id="event-starttime"]')
                startTime.clear()
                startTime.send_keys(self.stTime)
                endTime =self.driver.find_element(By.XPATH,'//*[@id="event-endtime"]')
                endTime.clear()
                # print (self.edTime)
                # endTime.send_keys(self.edTime)
                # time.sleep(13)
                
                self.driver.execute_script("arguments[0].value = '"+ self.edTime +"'", endTime)
                endTime.click()
                # roomNumber =self.driver.find_element(By.XPATH,'//*[@id="event-location"]')
                # roomNumber.clear()
                # roomNumber.send_keys("RB 2"+((str(0)+str(i-79)) if (i-79)<10 else str(i-79)))

                # check book status
                time.sleep(0.2)
                book_status = self.driver.find_element(By.ID,'event-button-save')
                if book_status.is_enabled() == False:
                    print ('invalid room 1'+ ((str(0)+str(i-64)) if (i-64)<10 else str(i-64)))
                    for i in range (1,3):
                        self.driver.back()
                    time.sleep(0.1)

                else:
                    counter_room +=1
                    print ('available room 1'+ ((str(0)+str(i-64)) if (i-64)<10 else str(i-64)))
                    self.resRoomNum = '1'+ ((str(0)+str(i-64)) if (i-64)<10 else str(i-64))

                    book_status.click()
                    
                    for i in range (1,2): # for i in range (1,2): # real env
                        self.driver.back()
                    time.sleep(0.1)

                    return True                   
            return False

            ### test code ###               
            if counter_room == 0:
                return False
            else:
                return True
        else: # given room number
            i = int(self.roomNum)-36
            EG_room = self.driver.find_element(By.ID,"chart-row-"+str(i)).find_element(By.CLASS_NAME,"event-location")
            EG_room.click()
            try:
                btn_book = self.driver.find_element(By.XPATH,'//*[@id="function-span"]/p['+str(8-delta_date)+']/a').click()
                # btn_book.click()
            except NoSuchElementException:
                self.driver.back()
                time.sleep(0.1)
                pass

            # Enter preset content
            startTime =self.driver.find_element(By.XPATH,'//*[@id="event-starttime"]')
            startTime.clear()
            startTime.send_keys(self.stTime_fm.strftime("%H:%M"))
            endTime =self.driver.find_element(By.XPATH,'//*[@id="event-endtime"]') 
            endTime.clear()
            self.driver.execute_script("arguments[0].value = '"+self.edTime+"'", endTime)
            # blank_area = self.driver.find_element(By.XPATH, '//*[@id="left-column"]/h1')
            endTime.click()
        
            # check book status
            time.sleep(0.2)
            book_status = self.driver.find_element(By.ID,'event-button-save')
            if book_status.is_enabled() == False:
                print ('invalid room '+ str(self.roomNum))

                for i in range (1,3):
                    self.driver.back()
                time.sleep(0.1)
                return False
            else:
                print ('available room '+ str(self.roomNum))
                self.resRoomNum = str(self.roomNum)
                # blank_area.click() # may can be deleted
                # book_status.click()

                for i in range (1,2): # for i in range (1,2): # real env
                    self.driver.back()
                time.sleep(0.1)
                return True

    def find_Termin_OG(self):
        print ("[find Termin in OG]")
        delta_date = (localtime+datetime.timedelta(days=7)-self.date_fm).days
        counter_room = 0
        # invalid_room = [82,85,90,93,94]
        invalid_room = [82]
        # time.sleep(0.5)
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        # to OG List
        btn_OG=self.driver.find_element(By.XPATH,'//*[@id="left-column"]/h2[2]/a').click()
        # actions = ActionChains(self.driver)
        # actions.move_to_element(btn_OG)
        # actions.click(btn_OG).perform()  

        if self.roomNum == 0: # no input of room number
            # fill the information of booking room
            for i in range (80,95):
                if (i not in invalid_room):
                    OG_room = self.driver.find_element(By.ID,"chart-row-"+str(i)).find_element(By.CLASS_NAME,"event-location")
                    # print (OG_room.text)
                    OG_room.click()
                    try:
                        btn_book = self.driver.find_element(By.XPATH,'//*[@id="function-span"]/p['+str(8-delta_date)+']/a').click()
                        # btn_book.click()
                    except NoSuchElementException:
                        print ('error: NoSuchElementException')
                        self.driver.back()
                        time.sleep(0.1)
                        continue 

                    # Enter preset content
                    startTime =self.driver.find_element(By.XPATH,'//*[@id="event-starttime"]')
                    startTime.clear()
                    startTime.send_keys(self.stTime)
                    endTime =self.driver.find_element(By.XPATH,'//*[@id="event-endtime"]')
                    # value = endTime.get_attribute("value") 
                    endTime.clear()
                    self.driver.execute_script("arguments[0].value = '"+self.edTime+"'", endTime)
                    
                    # blank_area = self.driver.find_element(By.XPATH, '//*[@id="left-column"]/h1')
                    endTime.click()
                    # endTime.send_keys(str(self.edTime_fm.hour)+':'+str(self.edTime_fm.minute))

                    # roomNumber =self.driver.find_element(By.XPATH,'//*[@id="event-location"]')
                    # roomNumber.clear()
                    # roomNumber.send_keys("RB 2"+((str(0)+str(i-79)) if (i-79)<10 else str(i-79)))
                    # check book status
                    time.sleep(0.2)
                    book_status = self.driver.find_element(By.ID,'event-button-save')
                    if book_status.is_enabled() == False:
                        print ('invalid room 2'+ ((str(0)+str(i-79)) if (i-79)<10 else str(i-79)))
                        for i in range (1,3):
                            self.driver.back()
                        time.sleep(0.1)
                    else:
                        print ('available room 2'+ ((str(0)+str(i-79)) if (i-79)<10 else str(i-79)))
                        self.resRoomNum = '2'+ ((str(0)+str(i-79)) if (i-79)<10 else str(i-79))
                        # blank_area.click() # may can be deleted
                        book_status.click()

                        for i in range (1,2): # for i in range (1,2): # real env
                            self.driver.back()
                        time.sleep(0.1)
                        
                        return True
            return False
            
            ### test code ###
            if counter_room == 0:
                return False
            else:
                return True
        else: # given room number
            i = int(self.roomNum)-121
            OG_room = self.driver.find_element(By.ID,"chart-row-"+str(i)).find_element(By.CLASS_NAME,"event-location")
            OG_room.click()
            try:
                btn_book = self.driver.find_element(By.XPATH,'//*[@id="function-span"]/p['+str(8-delta_date)+']/a').click()
                # btn_book.click()
            except NoSuchElementException:
                self.driver.back()
                time.sleep(0.1)
                pass

            # Enter preset content
            startTime =self.driver.find_element(By.XPATH,'//*[@id="event-starttime"]')
            startTime.clear()
            startTime.send_keys(self.stTime_fm.strftime("%H:%M"))
            endTime =self.driver.find_element(By.XPATH,'//*[@id="event-endtime"]') 
            endTime.clear()
            self.driver.execute_script("arguments[0].value = '"+self.edTime+"'", endTime)
            # blank_area = self.driver.find_element(By.XPATH, '//*[@id="left-column"]/h1')
            endTime.click()
        
            # check book status
            time.sleep(0.2)
            book_status = self.driver.find_element(By.ID,'event-button-save')
            if book_status.is_enabled() == False:
                print ('invalid room '+ str(self.roomNum))
                for i in range (1,3):
                    self.driver.back()
                time.sleep(0.1)
                return False
            else:
                print ('available room '+ str(self.roomNum))
                self.resRoomNum = str(self.roomNum)
                # blank_area.click() # may can be deleted
                # book_status.click()
                for i in range (1,2): # for i in range (1,2): # real env
                    self.driver.back()
                time.sleep(0.1)
                return True
    
    def extension_time(self):
        print ("[Extension time]")
        # btn_zeitplan = self.driver.find_element(By.XPATH,'//*[@id="my-activities"]')
        # btn_zeitplan.click()

        now = datetime.datetime.now(timezone)
        now_form = datetime.datetime.strptime(now.strftime("%H:%M"),"%H:%M") # only hour:minute
        # delta =self.date-localtime.day # differenz between desired day and today

        # go to the page of booked room
        print ("go to the page of booked room")

        # if the day to book in next month, need to click button
        if localtime.month!=self.date_fm.month: 
            print ('the day to book in next month, need to click button')
            self.driver.find_element(By.XPATH,'//*[@id="navigation-calendar"]/div/div/a[2]/span').click()

        btn_date = self.driver.find_element(By.XPATH,'//a[@class="ui-state-default" and text()="'+str(self.date_fm.day)+'"]')
        btn_date.click()
        btn_booked = self.driver.find_element(By.XPATH,'//div[@id="function-span"]/h1[2]/following-sibling::node()\
[position()<count(//div[@id="function-span"]/h1[2]/following-sibling::node())\
-count(//div[@id="function-span"]/h1[3]/following-sibling::node())]\
//p[contains(text(),\''+self.stTime+'\')]/../..//span[@class="event-link"]')
        btn_booked.click()

        # if date isn't todey+7 or end time < current time
        if self.date_fm.day!=(localtime+datetime.timedelta(days=7)).day or time_cmp(localtime,self.edTime_fm)>0: 
            print ("fill endTime textBox")
            endTime =self.driver.find_element(By.XPATH,'//*[@id="event-endtime"]')    
            endTime.clear()
            self.driver.execute_script("arguments[0].value = '"+self.edTime_fm.strftime("%H:%M")+"'", endTime)
            endTime.click()

            # check book status
            time.sleep(0.5)
            book_status = self.driver.find_element(By.ID,'event-button-save')
            if book_status.is_enabled() == True:
                book_status.click()
                self.bot.sendMsg("Successfully extended the room time to "+self.edTime_fm.strftime("%H:%M"))
                # print ("Successfully extended the room time to "+self.edTime_fm.strftime("%H:%M"))
                return True
            else:
                self.bot.sendMsg("Something wrong when extending room time, try next round")
                #  print ("Something wrong when extending room time, try next round")
                return False
        else: # date = today+7, start time < current time < end time
            # get value of end time in textBox
            print ("get value of end time in textBox")
            endTime =self.driver.find_element(By.XPATH,'//*[@id="event-endtime"]')
            ed_ori = datetime.datetime.strptime(endTime.get_attribute("value"),"%H:%M")
            ed_value = ed_ori
            ed_tmp = getNearestMinFor(now.strftime("%H:%M"))
            diff = diffMin( self.edTime_fm, ed_ori)
            round = int(diff/15)
            print ("next time to book: "+ ed_tmp.strftime("%H:%M"))
            
            # extend time in every 15 min
            for i in range(1,round+1):
                if (time_cmp(now,ed_ori)>0):

                    # if now>>value of endtime TextBox (over 15min) then book once, else waiting
                    if  diffMin(now_form,ed_value)>=15:
                        print ("now >> value of endtime TextBox (over 15min) ---> book once")
                        ed_tmp = getNearestMinBack(now.strftime("%H:%M"))
                    while (time_cmp(now,ed_tmp)<0):
                        print ("[" + now.strftime("%H:%M:%S")+"] Waiting until the next time slot opens, "+ str(round)+" round left")
                        time.sleep(13)
                        now = datetime.datetime.now(timezone)

                    # fill endTime textBox    
                    print ("fill endTime textBox")
                    endTime =self.driver.find_element(By.XPATH,'//*[@id="event-endtime"]')    
                    endTime.clear()
                    self.driver.execute_script("arguments[0].value = '"+ed_tmp.strftime("%H:%M")+"'", endTime)
                    endTime.click()


                    # check book status
                    time.sleep(0.5)
                    book_status = self.driver.find_element(By.ID,'event-button-save')
                    if book_status.is_enabled() == True:
                        self.bot.sendMsg("Successfully extended the room time to "+ed_tmp.strftime("%H:%M")+" ,"+ str(round-1)+" round left")

                        # refresh the time and end time (temporary)
                        print ("refresh the time and end time (temporary)")
                        now = datetime.datetime.now(timezone)
                        now_form = datetime.datetime.strptime(now.strftime("%H:%M"),"%H:%M") # only hour:minute
                        ed_tmp = getNearestMinFor(now.strftime("%H:%M"))
                        
                        # Calculate the number of remaining bookings
                        print ("Calculate the number of remaining bookings")
                        ed_value = datetime.datetime.strptime(endTime.get_attribute("value"),"%H:%M")
                        diff = diffMin(self.edTime_fm, ed_value)
                        round = int(diff/15)

                        # BOOKING...
                        book_status.click()

                        # if the booking is completed
                        if self.edTime_fm.hour==ed_value.hour and self.edTime_fm.minute==ed_value.minute:
                            self.bot.sendMsg("[Finished]")
                            # print ("[Finished]")
                            return True

                        # go back to the booking page
                        time.sleep(1)
                        self.driver.back()
                        print ("next time to book: "+ ed_tmp.strftime("%H:%M"))
                    else:
                        self.bot.sendMsg("Something wrong when extending room time, try next round")
                        now = datetime.datetime.now(timezone)
                        now_form = datetime.datetime.strptime(now.strftime("%H:%M"),"%H:%M") # only hour:minute
                        # return False
                else:
                    continue

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
    options.add_argument("--start-maximized")
    # options.add_argument("--window-size=1920,1080")

    bot = telebot.bot()

    intro = """Please choose mode:
    [1] Normal Mode
    [2] Extend your time"""
    # print (intro)
    # mode = int(input())
    # mode = 2

    if mode==1:
        # print("Enter your desired start time(example: 18:15): ")
        # st = input() # start time
        # print("Enter your end time:")    
        # et = input() # end time
        # print ("Enter your room number (if need):")
        # tmp_rm = input()
        # num_room= tmp_rm if tmp_rm else 0 # input room number if need
        # print ("Enter your wish date (if need, default value is today+7):")
        # tmp_dt = input()
        # date= tmp_dt if tmp_dt else 0 # input wish date if need

        # Input
        st = start_time
        et = end_time
        num_room = room_number
        date=date+'.'+str(localtime.year) if int(date)!=0 else str(localPlus.day)+'.'+str(localPlus.month)+'.'+str(localPlus.year)
        # format time
        st_form = datetime.datetime.strptime(st, "%H:%M")
        st_aft30 = st_form+datetime.timedelta(minutes=30)
        et_form = datetime.datetime.strptime(et, "%H:%M")
        ed_tmp = getNearestMinBack(localtime.strftime("%H:%M"))
        date_form = datetime.datetime.strptime(date,'%d.%m.%Y')

        # Pass parameters to the booker class
        data = ['https://hfm-karlsruhe.asimut.net/public/login.php',  '13200',  'ZXY200238zxy.',options, st,et,num_room,date]
        roombooker = booker(data)

        # Error input
        if date_form>(localtime_fm+datetime.timedelta(days=7)) or date_form<localtime_fm :
            print ('Your input date is overrange, please try to enter again.')
            exit()

        #  current time < (start time +30) and date = today+7
        s = 1
        while time_cmp(localtime,st_aft30)<0 and date_form==(localtime_fm+datetime.timedelta(days=7)):
            if (s==True):
                bot.sendMsg("[Situtation] current time < (start time +30)")
                bot.sendMsg("[" + localtime.strftime("%H:%M:%S")+"]"+" waiting until reservation is possible")
                s = 0
            print ("[" + localtime.strftime("%H:%M:%S")+"]"+" waiting until reservation is possible")
            time.sleep(13)
            
            # refresh
            localtime = datetime.datetime.now(timezone) 
            ed_tmp = getNearestMinBack(localtime.strftime("%H:%M"))

        roombooker.login()

        # current time > end time
        if time_cmp(localtime,et_form)>0:
            bot.sendMsg("[Situtation] current time > end time")
            if num_room==0:
                result = roombooker.find_Termin_EG() or roombooker.find_Termin_OG()
                # result =  roombooker.find_Termin_OG()
            else:
                result = roombooker.find_Termin_EG() if int(num_room) in range(101,116) else roombooker.find_Termin_OG() 
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
                    if num_room==0:
                        result = roombooker.find_Termin_EG() or roombooker.find_Termin_OG()
                    else:
                        result = roombooker.find_Termin_EG() if int(num_room) in range(101,116) else roombooker.find_Termin_OG()
                    if result:
                        bot.sendMsg("room booked in " + roombooker.resRoomNum + " from " + roombooker.stTime + " to "+ roombooker.edTime)
                        roombooker.edTime = et
                        roombooker.edTime_fm = et_form
                        result_ex = roombooker.extension_time()
                        if result_ex: break
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
    elif mode ==2:
        # input: date(default:+7),start time(default:now), desired end time
        # print ("Enter your wish date (default: today+7):")
        # tmp_dt = input()
        # date= tmp_dt if tmp_dt else 0 # input wish date if need
        # print("Enter your start time(format: 18:15):")
        # st = input() # start time
        # print("Enter your desired end time:")    
        # et = input() # end time

        # Input
        date=date+'.'+str(localtime.year) if date!='0' else str(localPlus.day)+'.'+str(localPlus.month)+'.'+str(localPlus.year)
        st = start_time
        et = end_time
        num_room= room_number # default
        
        data = ['https://hfm-karlsruhe.asimut.net/public/login.php',  '13200',  'ZXY200238zxy.',options, st,et,num_room,date]
        roombooker = booker(data)
        roombooker.login()
        roombooker.extension_time()

    # 退出浏览器
    roombooker.driver.quit()
