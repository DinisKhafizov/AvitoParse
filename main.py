import ssl
import requests
from lxml import html
import time
from bs4 import BeautifulSoup as soup
import telebot

from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util import ssl_

CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""

class TlsAdapter(HTTPAdapter):

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)

token = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(token)

session = requests.session()
adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
session.mount("https://", adapter)

url = 'YOUR_URL_IN_AVITO'
id = 'YOUR_TELEGRAM_ID'
txtfile = 'YOUR_TXT_FIL_FOR_SAVING_INFO'
class_for_links = 'CLASS_IN_WEB_GTML_FOR_FINDING'

while True:
    page = session.get(url)
    bs = soup(page.text, 'lxml')
    links = bs.find_all(class_=class_for_links)
    for i in range(len(links)):
        links[i] = 'https://www.avito.ru' + links[i].get('href')
    file = open(txtfile, 'r' ).read().split()
    for i in range(len(links)):
        if links[i] not in file:
          with open(txtfile, 'a') as f:
              f.write(links[i])
              f.write('\n')
              bot.send_message(id, links[i])
    time.sleep(120)

bot.polling(none_stop=True, interval=0)
