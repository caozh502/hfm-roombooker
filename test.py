# print("Goodbye, World!")
import requests

url = 'https://hfm-karlsruhe.asimut.net/public/login.php'
header = { 'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
}

from_data = {'authenticate-useraccount': '13200',
    'authenticate-password': 'ZXY200238zxy.',
    'authenticate-url': '/public/',
    'authenticate-verification': 'ok',
    # 'execution': 'e1s1',
    # '_eventId': 'submit',
    # 'submit': '登录'
}
s = requests.session()
response = s.post(url, data = from_data, headers = header)
if 'Xinyuan Zhang' in response.content.decode('utf-8'):
    print ('successfully login')
else:
    print ('failed login')
