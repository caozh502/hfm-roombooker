from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import datetime

class booker:
    def __init__(self,data):
        self.url = data[0]
        self.acc = data[1]
        self.psw = data[2]
        self.opt = data[3]
        self.stTime = data[4]
        self.edTime = data[5]
        self.roomNum = data[6]
        self.resRoomNum = '0'
        localtime = time.localtime(time.time())
        self.mday = localtime.tm_mday+7   

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
        time.sleep(0.5)

        # ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        btn_EG=self.driver.find_element(By.XPATH,'//*[@id="left-column"]/h2[1]/a')
        btn_EG.click()
        # actions = ActionChains(self.driver)



        # actions.click(EG_room).perform()

    def find_Termin_OG(self):
        invalid_room = [85,90,93,94]
        # time.sleep(0.5)
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        # to OG List
        btn_OG=self.driver.find_element(By.XPATH,'//*[@id="left-column"]/h2[2]/a')
        actions = ActionChains(self.driver)
        actions.move_to_element(btn_OG)
        actions.click(btn_OG).perform()  

        # fill the information of booking room
        for i in range (80,95):
            if (i not in invalid_room):
                OG_room = self.driver.find_element(By.ID,"chart-row-"+str(i)).find_element(By.CLASS_NAME,"event-location")
                # print (OG_room.text)
                OG_room.click()
                btn_book = self.driver.find_element(By.XPATH,'//*[@id="function-span"]/p[8]/a')
                btn_book.click()

                # Enter preset content
                startTime =self.driver.find_element(By.XPATH,'//*[@id="event-starttime"]')
                startTime.clear()
                startTime.send_keys(str(self.stTime.hour)+':'+str(self.stTime.minute))
                endTime =self.driver.find_element(By.XPATH,'//*[@id="event-endtime"]')
                # value = endTime.get_attribute("value") 
                endTime.clear()
                self.driver.execute_script("arguments[0].value = '"+str(self.edTime.hour)+':'+str(self.edTime.minute)+"'", endTime)
                
                blank_area = self.driver.find_element(By.XPATH, '//*[@id="left-column"]/h1')
                endTime.click()
                # endTime.send_keys(str(self.edTime.hour)+':'+str(self.edTime.minute))

                # roomNumber =self.driver.find_element(By.XPATH,'//*[@id="event-location"]')
                # roomNumber.clear()
                # roomNumber.send_keys("RB 2"+((str(0)+str(i-79)) if (i-79)<10 else str(i-79)))
                # check book status
                # time.sleep(1)
                book_status = self.driver.find_element(By.ID,'event-button-save')
                if book_status.is_enabled() == False:
                    print ('invalid room 2'+ ((str(0)+str(i-79)) if (i-79)<10 else str(i-79)))
                    for i in range (1,3):
                        self.driver.back()
                else:
                    print ('available room 2'+ ((str(0)+str(i-79)) if (i-79)<10 else str(i-79)))
                    self.resRoomNum = '2'+ ((str(0)+str(i-79)) if (i-79)<10 else str(i-79))
                    blank_area.click()
                    # book_status.click()
                    # for i in range (1,3):
                    #     self.driver.back()
                    # return True
        return False
def time_cmp(first_time, second_time):
    return (int(first_time.strftime("%H%M")) - int(second_time.strftime("%H%M")))

if __name__ == '__main__':
    # ignore some errors
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    localtime = datetime.datetime.now()
    
    ## valid after all works done
    # options.add_argument('--headless')
    # options.add_argument("--start-maximized")
    # options.add_argument("--window-size=1920,1080")

    # print("Enter your wish start time(example: 18:15): ")
    # st = input() # start time
    # print("Enter your duration(h):")    
    # et = input() # end time
    # print ("Enter your room number (if need):")
    # tmp = input()
    # num_room= tmp if tmp else 0 # input room number if need
    st ="20:00"
    st_form = datetime.datetime.strptime(st, "%H:%M")
    st_before = st_form-datetime.timedelta(minutes=30)
    et ="20:30"
    et_form = datetime.datetime.strptime(et, "%H:%M")
    num_room= "210"
    data = ['https://hfm-karlsruhe.asimut.net/public/login.php',  '13200',  'ZXY200238zxy.',options, st_form,et_form,num_room]
    roombooker = booker(data)
    roombooker.login()

    # current time > end time
    if time_cmp(localtime,et_form)>0: 
        # result = roombooker.find_Termin_EG() and roombooker.find_Termin_OG()
        result = roombooker.find_Termin_OG()
        if result:
            print ("room booked in " + roombooker.resRoomNum + " from " + 
            str(roombooker.stTime.hour)+':'+str(roombooker.stTime.minute) + " to "+ 
            str(roombooker.edTime.hour)+':'+str(roombooker.edTime.minute))
        else:
            print ("Cannot find empty room at moment")
    else:
        #  (start time +30) < current time < end time
        if time_cmp(localtime,et_form)<0 and time_cmp(localtime,st_before)>0:
            print (2)
            # result = roombooker.find_Termin_EG() and roombooker.find_Termin_OG()
            # if result:
            #     print ("room found in " + str(roombooker.resRoomNum) + " from " + str(roombooker.stTime) + " to "+ str(roombooker.edTime))
            # else:
            #     print ("Cannot find empty room at moment")
        else:
            #  current time < (start time +30)
            if time_cmp(localtime,st_before)<0:
                print ("waiting now until reservation is possible")
                time.sleep(15)
                
    # 退出浏览器
    # roombooker.driver.quit()
