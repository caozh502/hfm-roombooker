from xmlrpc.client import DateTime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import datetime

def time_cmp(first_time, second_time):
    return (int(first_time.strftime("%H%M")) - int(second_time.strftime("%H%M")))

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
        localtime = time.localtime(time.time())
        self.today = localtime.tm_mday
        
        self.url = data[0]
        self.acc = data[1]
        self.psw = data[2]
        self.opt = data[3]
        self.stTime = datetime.datetime.strptime(data[4], "%H:%M")
        self.edTime = datetime.datetime.strptime(data[5], "%H:%M")
        self.roomNum = data[6]
        self.date = int(data[7]) if data[7]!=0 else self.today+7
        self.resRoomNum = '0'
        
        

    def login(self):   

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
        # time.sleep(0.5)
        delta_date = (self.today+7) - self.date   
        counter_room = 0
        # invalid_room = [65,67,73,75]
        invalid_room = []
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        btn_EG=self.driver.find_element(By.XPATH,'//*[@id="left-column"]/h2[1]/a')
        btn_EG.click()
        
        if self.roomNum == 0: # no input of room number
            for i in range (65,80):
                if (i not in invalid_room):
                    EG_room = self.driver.find_element(By.ID,"chart-row-"+str(i)).find_element(By.CLASS_NAME,"event-location")
                    EG_room.click()
                    btn_book = self.driver.find_element(By.XPATH,'//*[@id="function-span"]/p['+str(8-delta_date)+']/a')
                    btn_book.click()

                    # Enter preset content
                    startTime =self.driver.find_element(By.XPATH,'//*[@id="event-starttime"]')
                    startTime.clear()
                    startTime.send_keys(self.stTime.strftime("%H:%M"))
                    endTime =self.driver.find_element(By.XPATH,'//*[@id="event-endtime"]')
                    # value = endTime.get_attribute("value") 
                    endTime.clear()
                    self.driver.execute_script("arguments[0].value = '"+self.edTime.strftime("%H:%M")+"'", endTime)
                    
                    # blank_area = self.driver.find_element(By.XPATH, '//*[@id="left-column"]/h1')
                    endTime.click()
                    # endTime.send_keys(str(self.edTime.hour)+':'+str(self.edTime.minute))
                
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
                    else:
                        counter_room +=1
                        print ('available room 1'+ ((str(0)+str(i-64)) if (i-64)<10 else str(i-64)))
                        self.resRoomNum = '1'+ ((str(0)+str(i-64)) if (i-64)<10 else str(i-64))
                        # blank_area.click() # may can be deleted
                        # book_status.click()
                        
                        for i in range (1,3): # for i in range (1,2): # real env
                            self.driver.back()

                        # return True
            # return False

            ### test code ###               
            if counter_room == 0:
                return False
            else:
                return True
        else: # given room number
            i = int(self.roomNum)-36
            EG_room = self.driver.find_element(By.ID,"chart-row-"+str(i)).find_element(By.CLASS_NAME,"event-location")
            EG_room.click()
            btn_book = self.driver.find_element(By.XPATH,'//*[@id="function-span"]/p['+str(8-delta_date)+']/a')
            btn_book.click()

            # Enter preset content
            startTime =self.driver.find_element(By.XPATH,'//*[@id="event-starttime"]')
            startTime.clear()
            startTime.send_keys(self.stTime.strftime("%H:%M"))
            endTime =self.driver.find_element(By.XPATH,'//*[@id="event-endtime"]') 
            endTime.clear()
            self.driver.execute_script("arguments[0].value = '"+self.edTime.strftime("%H:%M")+"'", endTime)
            # blank_area = self.driver.find_element(By.XPATH, '//*[@id="left-column"]/h1')
            endTime.click()
        
            # check book status
            time.sleep(0.2)
            book_status = self.driver.find_element(By.ID,'event-button-save')
            if book_status.is_enabled() == False:
                print ('invalid room '+ str(self.roomNum))

                for i in range (1,3):
                    self.driver.back()
                return False
            else:
                print ('available room '+ str(self.roomNum))
                self.resRoomNum = str(self.roomNum)
                # blank_area.click() # may can be deleted
                # book_status.click()

                for i in range (1,3): # for i in range (1,2): # real env
                    self.driver.back()
                return True

    def find_Termin_OG(self):
        delta_date = (self.today+7) - self.date 
        counter_room = 0
        # invalid_room = [82,85,90,93,94]
        invalid_room = [82]
        # time.sleep(0.5)
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        # to OG List
        btn_OG=self.driver.find_element(By.XPATH,'//*[@id="left-column"]/h2[2]/a')
        actions = ActionChains(self.driver)
        actions.move_to_element(btn_OG)
        actions.click(btn_OG).perform()  

        if self.roomNum == 0: # no input of room number
            # fill the information of booking room
            for i in range (80,95):
                if (i not in invalid_room):
                    OG_room = self.driver.find_element(By.ID,"chart-row-"+str(i)).find_element(By.CLASS_NAME,"event-location")
                    # print (OG_room.text)
                    OG_room.click()
                    btn_book = self.driver.find_element(By.XPATH,'//*[@id="function-span"]/p['+str(8-delta_date)+']/a')
                    btn_book.click()

                    # Enter preset content
                    startTime =self.driver.find_element(By.XPATH,'//*[@id="event-starttime"]')
                    startTime.clear()
                    startTime.send_keys(self.stTime.strftime("%H:%M"))
                    endTime =self.driver.find_element(By.XPATH,'//*[@id="event-endtime"]')
                    # value = endTime.get_attribute("value") 
                    endTime.clear()
                    self.driver.execute_script("arguments[0].value = '"+self.edTime.strftime("%H:%M")+"'", endTime)
                    
                    # blank_area = self.driver.find_element(By.XPATH, '//*[@id="left-column"]/h1')
                    endTime.click()
                    # endTime.send_keys(str(self.edTime.hour)+':'+str(self.edTime.minute))

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
                    else:
                        print ('available room 2'+ ((str(0)+str(i-79)) if (i-79)<10 else str(i-79)))
                        self.resRoomNum = '2'+ ((str(0)+str(i-79)) if (i-79)<10 else str(i-79))
                        # blank_area.click() # may can be deleted
                        # book_status.click()

                        for i in range (1,3): # for i in range (1,2): # real env
                            self.driver.back()
                        
                        # return True
            # return False
            
            ### test code ###
            if counter_room == 0:
                return False
            else:
                return True
        else: # given room number
            i = int(self.roomNum)-121
            OG_room = self.driver.find_element(By.ID,"chart-row-"+str(i)).find_element(By.CLASS_NAME,"event-location")
            OG_room.click()
            btn_book = self.driver.find_element(By.XPATH,'//*[@id="function-span"]/p['+str(8-delta_date)+']/a')
            btn_book.click()

            # Enter preset content
            startTime =self.driver.find_element(By.XPATH,'//*[@id="event-starttime"]')
            startTime.clear()
            startTime.send_keys(self.stTime.strftime("%H:%M"))
            endTime =self.driver.find_element(By.XPATH,'//*[@id="event-endtime"]') 
            endTime.clear()
            self.driver.execute_script("arguments[0].value = '"+self.edTime.strftime("%H:%M")+"'", endTime)
            # blank_area = self.driver.find_element(By.XPATH, '//*[@id="left-column"]/h1')
            endTime.click()
        
            # check book status
            time.sleep(0.2)
            book_status = self.driver.find_element(By.ID,'event-button-save')
            if book_status.is_enabled() == False:
                print ('invalid room '+ str(self.roomNum))
                for i in range (1,3):
                    self.driver.back()
                return False
            else:
                print ('available room '+ str(self.roomNum))
                self.resRoomNum = str(self.roomNum)
                # blank_area.click() # may can be deleted
                # book_status.click()
                for i in range (1,3): # for i in range (1,2): # real env
                    self.driver.back()
                return True
    
    def extension_time(self):
        btn_zeitplan = self.driver.find_element(By.XPATH,'//*[@id="my-activities"]')
        btn_zeitplan.click()

        now = datetime.datetime.now()
        now_form = datetime.datetime.strptime(now.strftime("%H:%M"),"%H:%M") # only hour:minute
        delta =self.date-self.today # differenz between desired day and today

        # to the page of booked room
        btn_booked = self.driver.find_element(By.XPATH,'//div[@id="function-span"]/h1['+str(2+delta)+']/following-sibling::node()\
[position()<count(//div[@id="function-span"]/h1['+str(2+delta)+']/following-sibling::node())\
-count(//div[@id="function-span"]/h1['+str(2+delta+1)+']/following-sibling::node())]\
//p[contains(text(),\''+self.stTime.strftime("%H:%M")+'\')]/../..//span[@class="event-link"]') if self.date !=0 else \
                        self.driver.find_element(By.XPATH,'//div[@id="function-span"]/h1[9]/following-sibling::node()')
        btn_booked.click()
        # get value of end time in textBox
        endTime =self.driver.find_element(By.XPATH,'//*[@id="event-endtime"]')
        ed_ori = datetime.datetime.strptime(endTime.get_attribute("value"),"%H:%M")
        ed_value = ed_ori
        ed_tmp = getNearestMinFor(now.strftime("%H:%M"))
        diff = diffMin( self.edTime, ed_ori)
        round = int(diff/15)

        # extend time in every 15 min
        for i in range(1,round+1):
            if (time_cmp(now,ed_ori)>0):

                # if now>>value of endtime TextBox (over 15min) then book once, else waiting
                if  diffMin(now_form,ed_value)>=15:
                    ed_tmp = getNearestMinBack(now.strftime("%H:%M"))
                while (time_cmp(now,ed_tmp)<0):
                # for m in range(1,2):
                    print ("[" + now.strftime("%H:%M:%S")+"] waiting now until next reservation is possible, "+ str(round)+" round left")
                    time.sleep(15)
                    now = datetime.datetime.now()

                # fill endTime textBox    
                endTime =self.driver.find_element(By.XPATH,'//*[@id="event-endtime"]')    
                endTime.clear()
                self.driver.execute_script("arguments[0].value = '"+ed_tmp.strftime("%H:%M")+"'", endTime)
                endTime.click()


                # check book status
                time.sleep(0.5)
                book_status = self.driver.find_element(By.ID,'event-button-save')
                if book_status.is_enabled() == True:
                    print ("Successfully extended the room time to "+ed_tmp.strftime("%H:%M"))

                    # refresh the time and end time (temporary)
                    now = datetime.datetime.now()
                    now_form = datetime.datetime.strptime(now.strftime("%H:%M"),"%H:%M") # only hour:minute
                    ed_tmp = getNearestMinFor(now.strftime("%H:%M"))
                    
                    # Calculate the number of remaining bookings
                    ed_value = datetime.datetime.strptime(endTime.get_attribute("value"),"%H:%M")
                    diff = diffMin(self.edTime, ed_value)
                    round = int(diff/15)

                    # BOOKING...
                    book_status.click()

                    # if the booking is completed
                    if self.edTime.hour==ed_value.hour and self.edTime.minute==ed_value.minute:
                        print ("[Finished]")
                        return True

                    # go back to the booking page
                    time.sleep(1)
                    self.driver.back()
                    print ("next time to book: "+ ed_tmp.strftime("%H:%M"))
                else:
                    print ("Something wrong when extending room time, try next round")
                    now = datetime.datetime.now()
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

    localtime = datetime.datetime.now()

    
    ## headless, no window
    options.add_argument('--headless')
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    intro = """Please choose mode:
    [1] normal
    [2] extend your time"""
    # print (intro)
    # mode = int(input())
    mode = 2
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
        st ="17:15"
        st_form = datetime.datetime.strptime(st, "%H:%M")
        st_aft45 = st_form+datetime.timedelta(minutes=45)
        et ="18:30"
        et_form = datetime.datetime.strptime(et, "%H:%M")
        num_room= 0 # str or 0(default)
        date = 0 # str or 0(default)
        data = ['https://hfm-karlsruhe.asimut.net/public/login.php',  '13200',  'ZXY200238zxy.',options, st,et,num_room,date]
        roombooker = booker(data)

        # Error input
        if (localtime.day+7)<int(date):
            print ('Your input date is overrange, please try to enter again.')

        #  current time < (start time +45) and date = today+7
        while time_cmp(localtime,st_aft45)<0 and ((localtime.day+7)==(int(date)) or date==0):
            print ("[" + localtime.strftime("%H:%M:%S")+"]"+" waiting now until reservation is possible")
            time.sleep(15)
            localtime = datetime.datetime.now() # refresh
        roombooker.login()
        # current time > end time
        if time_cmp(localtime,et_form)>0:
            print ("Situtation: current time > end time")
            if num_room==0:
                result = roombooker.find_Termin_EG() or roombooker.find_Termin_OG()
            else:
                result = roombooker.find_Termin_EG() if int(num_room) in range(101,116) else roombooker.find_Termin_OG() 
            if result:
                # print ("room booked in " + roombooker.resRoomNum + " from " + 
                # str(roombooker.stTime.hour)+':'+str(roombooker.stTime.minute) + " to "+ 
                # str(roombooker.edTime.hour)+':'+str(roombooker.edTime.minute))
                print ("room booked in " + roombooker.resRoomNum + " from " + 
                roombooker.stTime.strftime("%H:%M") + " to "+ roombooker.edTime.strftime("%H:%M"))
            else:
                print ("Cannot find empty room at moment")
        #  (start time +45) < current time < end time
        else:
            if time_cmp(localtime,et_form)<0 and time_cmp(localtime,st_aft45)>0:
                print ("Situtation: (start time +45) < current time < end time")
                ed_tmp=getNearestMinBack(localtime.strftime("%H:%M"))
                roombooker.edTime = ed_tmp
                print (roombooker.edTime.strftime("%H:%M"))
                if num_room==0:
                    result = roombooker.find_Termin_EG() or roombooker.find_Termin_OG()
                else:
                    result = roombooker.find_Termin_EG() if int(num_room) in range(101,116) else roombooker.find_Termin_OG()
                if result:
                    print ("room booked in " + roombooker.resRoomNum + " from " + 
                    roombooker.stTime.strftime("%H:%M") + " to "+ roombooker.edTime.strftime("%H:%M"))
                    roombooker.edTime = et_form
                    roombooker.extension_time()
                else: # try again
                    print ("Cannot find empty room at moment, try again...")
                    time.sleep(15)
                    result = roombooker.find_Termin_EG() or roombooker.find_Termin_OG()
                    if result:
                        print ("room booked in " + roombooker.resRoomNum + " from " + 
                        roombooker.stTime.strftime("%H:%M") + " to "+ roombooker.edTime.strftime("%H:%M"))
                        roombooker.edTime = et_form
                        roombooker.extension_time()
                    else:
                        print ("Cannot find empty room at moment, please try in another time :(")
        
            
        # if (localtime.day+7)==(int(date)) or date==0:
        #     roombooker.login()
        #     # current time > end time
        #     if time_cmp(localtime,et_form)>0: 
        #         if num_room==0:
        #             result = roombooker.find_Termin_EG() or roombooker.find_Termin_OG()
        #         else:
        #             result = roombooker.find_Termin_EG() if int(num_room) in range(101,116) else roombooker.find_Termin_OG() 
        #         if result:
        #             # print ("room booked in " + roombooker.resRoomNum + " from " + 
        #             # str(roombooker.stTime.hour)+':'+str(roombooker.stTime.minute) + " to "+ 
        #             # str(roombooker.edTime.hour)+':'+str(roombooker.edTime.minute))
        #             print ("room booked in " + roombooker.resRoomNum + " from " + 
        #             roombooker.stTime.strftime("%H:%M") + " to "+ roombooker.edTime.strftime("%H:%M"))
        #         else:
        #             print ("Cannot find empty room at moment")
        #     else:
        #         #  (start time +45) < current time < end time
        #         if time_cmp(localtime,et_form)<0 and time_cmp(localtime,st_aft45)>0:
        #             ed_tmp=getNearestMinBack(localtime.strftime("%H:%M"))
        #             roombooker.edTime = ed_tmp
        #             if num_room==0:
        #                 result = roombooker.find_Termin_EG() or roombooker.find_Termin_OG()
        #             else:
        #                 result = roombooker.find_Termin_EG() if int(num_room) in range(101,116) else roombooker.find_Termin_OG()
        #             if result:
        #                 print ("room booked in " + roombooker.resRoomNum + " from " + 
        #                 roombooker.stTime.strftime("%H:%M") + " to "+ roombooker.edTime.strftime("%H:%M"))
        #                 roombooker.edTime = et_form
        #                 roombooker.extension_time()
        #             else: # try again
        #                 print ("Cannot find empty room at moment, try again...")
        #                 time.sleep(15)
        #                 result = roombooker.find_Termin_EG() or roombooker.find_Termin_OG()
        #                 if result:
        #                     print ("room booked in " + roombooker.resRoomNum + " from " + 
        #                     roombooker.stTime.strftime("%H:%M") + " to "+ roombooker.edTime.strftime("%H:%M"))
        #                     roombooker.edTime = et_form
        #                     roombooker.extension_time()
        #                 else:
        #                     print ("Cannot find empty room at moment, please try in another time :(")
        #             # result = roombooker.find_Termin_EG() and roombooker.find_Termin_OG()
        #             # if result:
        #             #     print ("room found in " + str(roombooker.resRoomNum) + " from " + str(roombooker.stTime) + " to "+ str(roombooker.edTime))
        #             # else:
        #             #     print ("Cannot find empty room at moment")
        #         # else:

        # else:
        #     if (localtime.day+7)>int(date):
        #         roombooker.login()
        #         if num_room==0:
        #             result = roombooker.find_Termin_EG() or roombooker.find_Termin_OG()
        #         else:
        #             result = roombooker.find_Termin_EG() if int(num_room) in range(101,116) else roombooker.find_Termin_OG() 
        #         if result:
        #             print ("room booked in " + roombooker.resRoomNum + " from " + 
        #             roombooker.stTime.strftime("%H:%M") + " to "+ roombooker.edTime.strftime("%H:%M"))
        #         else:
        #             print ("Cannot find empty room at moment")
        #     else:
        #         if (localtime.day+7)<int(date):
        #             print ('Your input date is false, please try to enter again.')
    elif mode ==2:
        # input: day(default:+7),start time(default:now), desired end time, switch time between two room(No consideration for now)
        # print ("Enter your wish date (default: today+7):")
        # tmp_dt = input()
        # date= tmp_dt if tmp_dt else 0 # input wish date if need
        # print("Enter your start time(format: 18:15):")
        # st = input() # start time
        # print("Enter your desired end time:")    
        # et = input() # end time

        date = "17"
        st ="21:00"
        st_form = datetime.datetime.strptime(st, "%H:%M")
        # st_before = st_form-datetime.timedelta(minutes=45)
        et ="23:30"
        et_form = datetime.datetime.strptime(et, "%H:%M")
        num_room= 0
        
        # print ("still under working...")
        
        data = ['https://hfm-karlsruhe.asimut.net/public/login.php',  '13200',  'ZXY200238zxy.',options, st,et,num_room,date]
        roombooker = booker(data)
        roombooker.login()
        roombooker.extension_time()

    

    
                
    # 退出浏览器
    # roombooker.driver.quit()
