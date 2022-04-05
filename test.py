# print("Goodbye, World!")
import requests

url = 'https://hfm-karlsruhe.asimut.net/public/login.php'
header = { 'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
}

from_data = {'username': '13200',
    'password': 'ZXY200238zxy.',
    'code': '',
    'lt': 'xxx',
    'execution': 'e1s1',
    '_eventId': 'submit',
    'submit': '登录'
}
s = requests.session()
response = s.post(url, data = from_data, headers = header)
print response.status_code