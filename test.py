
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

class booker:
    def __init__(self,data):
        self.url = data[0]
        self.acc = data[1]
        self.psw = data[2]
        self.stTime = data[3]
        self.opt = data[4]

    def login(self):   

        # set chromedriver
        self.driver=webdriver.Chrome(chrome_options=self.opt)
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
        btn_EG=self.driver.find_element(By.XPATH,'//*[@id="left-column"]/h2[1]/a')
        btn_EG.click()


if __name__ == '__main__':
    # ignore some errors
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    print("Enter your wish time:")
    t = input()
    data = ['https://hfm-karlsruhe.asimut.net/public/login.php',  '13200',  'ZXY200238zxy.',t,options]
    roombooker = booker(data)
    roombooker.login()
    roombooker.find_Termin_EG()
    # 退出浏览器
    roombooker.driver.quit()
