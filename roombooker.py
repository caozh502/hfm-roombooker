import time
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import telebot
import pytz
import numpy as np

utc=pytz.UTC
timezone = pytz.timezone("Europe/Berlin")
localtime = datetime.datetime.now(timezone)

invalid_room_EG = np.array([114]) # EG: [65-79]
invalid_room_OG = np.array([203]) # OG: [80-94]

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
        self.counter = 0
        

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
        invalid_room = invalid_room_EG - 36
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        btn_EG=self.driver.find_element(By.XPATH,'//*[@id="left-column"]/h2[1]/a').click()
        # btn_EG.click()
        
        if self.roomNum == 0: # no input of room number
            for i in range (65,80):
                if (i not in invalid_room): 
                    EG_room = self.driver.find_element(By.ID,"chart-row-"+str(i)).find_element(By.CLASS_NAME,"event-location").click()
                try:
                    btn_book = self.driver.find_element(By.XPATH,'//*[@id="function-span"]/p['+str(8-delta_date)+']/a').click()
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
                    # print ('invalid room 1'+ ((str(0)+str(i-64)) if (i-64)<10 else str(i-64)))
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
        invalid_room = invalid_room_OG - 121
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
                        # print ('invalid room 2'+ ((str(0)+str(i-79)) if (i-79)<10 else str(i-79)))
                        for i in range (1,3):
                            self.driver.back()
                        time.sleep(0.1)
                    else:
                        print ('available room 2'+ ((str(0)+str(i-79)) if (i-79)<10 else str(i-79)))
                        self.resRoomNum = '2'+ ((str(0)+str(i-79)) if (i-79)<10 else str(i-79))
                        
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
                        print ("now >> endtime in TextBox (over 15min) ---> book once")
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
                        self.bot.sendMsg("Successfully extended the room time to "+ed_tmp.strftime("%H:%M")+", "+ str(round-1)+" round left")

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
                    print ("time_cmp(now,ed_ori)<0")
                    print (now)
                    print (ed_ori)
                    continue
