
# import requests

# url = 'https://hfm-karlsruhe.asimut.net/public/login.php'
# header = { 'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
# }

# from_data = {'authenticate-useraccount': '13200',
#     'authenticate-password': 'ZXY200238zxy.',
#     'authenticate-url': '/public/',
#     'authenticate-verification': 'ok',
#     # 'execution': 'e1s1',
#     # '_eventId': 'submit',
#     # 'submit': '登录'
# }
# s = requests.session()
# response = s.post(url, data = from_data, headers = header)

# if 'Xinyuan Zhang' in response.content.decode('utf-8'):
#     print ('successfully login')
# else:
#     print ('failed login')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time

class booker:
    def __init__(self,data):
        self.url = data[0]
        self.acc = data[1]
        self.psw = data[2]
        self.stTime = data[3]
        self.dur = data[4]
        self.opt = data[5]

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
        actions = ActionChains(self.driver)
        # for i in range(65,65):
        EG_room = self.driver.find_element(By.XPATH,'//*[@id="left-column"]/h2[2]/a')
        actions.move_to_element(EG_room)
        # actions.click(EG_room).perform()

    def find_Termin_OG(self):
        invalid_room = [85,90,93,94]
        time.sleep(0.5)
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        btn_OG=self.driver.find_element(By.XPATH,'//*[@id="left-column"]/h2[2]/a')
        actions = ActionChains(self.driver)
        actions.move_to_element(btn_OG)
        actions.click(btn_OG).perform()  
        for i in range (80,94):
            if (i not in invalid_room):
                OG_room = self.driver.find_element(By.ID,"chart-row-"+str(i)).find_element(By.CLASS_NAME,"event-location")
                # print (OG_room.text)
                OG_room.click()
                btn_book = self.driver.find_element(By.XPATH,'//*[@id="function-span"]/p[8]/a')
                btn_book.click()
                book_status = self.driver.find_element(By.ID,'event-button-save')
                if book_status.is_enabled() == False:
                    print ('invalid room 2'+ ((str(0)+str(i-79)) if (i-79)<10 else str(i-79)))
                    for i in range (1,3):
                        self.driver.back()
                else:
                    print ('invalid room 2'+ ((str(0)+str(i-79)) if (i-79)<10 else str(i-79)))
                    for i in range (1,3):
                        self.driver.back()


if __name__ == '__main__':
    # ignore some errors
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    # print("Enter your wish start time(example: 18:15): ")
    # st = input()
    # print("Enter your duration(h):")    
    # dur = input()
    st =0
    dur =0
    data = ['https://hfm-karlsruhe.asimut.net/public/login.php',  '13200',  'ZXY200238zxy.',st,dur,options]
    roombooker = booker(data)
    roombooker.login()
    roombooker.find_Termin_OG()
    # 退出浏览器
    # roombooker.driver.quit()
