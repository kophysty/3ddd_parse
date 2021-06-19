import requests
from bs4 import BeautifulSoup
from twocaptcha import TwoCaptcha

info = {'token': input('Your token is: '), 'email': input('Your email is: '), 'password': input('Your password is: ')}

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find('input', attrs={'name': '_csrf_token'})
    csrf = item['value']
    return csrf

solver = TwoCaptcha(info['token'])
g_recaptcha = ''
try:
    result = solver.recaptcha(
        sitekey='6LftX68ZAAAAAOvXzEPz4lx9jgzfHdU3uVj-ptKT',
        url='https://3ddd.ru/login',
        invisible=1)

except Exception as e:
    exit(e)
else:
    g_recaptcha = result['code']

header = {
    # 'user-agent': user
}

url = 'https://3ddd.ru/login'
url_form = 'https://3ddd.ru/login_check'

loging = requests.get(url, headers=header)
loging_cookies = loging.cookies
login_csrf = get_content(loging.text)

datas = {
    '_username': info['email'],
    '_password': info['password'],
    '_csrf_token': login_csrf,
    'g-recaptcha-response': g_recaptcha
}

session = requests.Session()


goToLog = session.post(url_form, data=datas, headers=header, cookies=loging_cookies)

