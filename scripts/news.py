from pprint import pprint
import requests
import os
import json


# ЗАГОЛОВОК ЗАПРОСА
head = {
        'cookie': '_ga=GA1.2.52789296.1648979760; cookiePrivacyPreferenceBannerProduction=notApplicable;'
                  ' cookiesSettings={"analytics":true,"advertising":true}; g_state={"i_p":1666534732393,'
                  '"i_l":4}; _gid=GA1.2.329261428.1664702353; _sp_ses.cf1a=*; _gat_gtag_UA_24278967_1=1;'
                  ' _sp_id.cf1a=20b4efa2-04fb-4650-8cef-f25885fcba00.1648979760.21.1664717312.1664710231.'
                  'c311379f-2752-4ec1-b5c3-c409fa3bbe91',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/104.0.5112.114 Safari/537.36'}


# ПОЛУЧЕНИЕ СПИСКА НОВОСТЕЙ
def get_news(b, logoid, im):
    r = requests.get(f'https://news-headlines.tradingview.com/headlines/'
                     f'?category=stock&lang=ru&symbol={b}%3A{logoid}', headers=head)
    if im and not os.path.exists(f'icons/{im}.svg'):
        img_data = requests.get(f'https://s3-symbol-logo.tradingview.com/{im}--big.svg').content
        with open(f'icons/{im}.svg', 'wb') as handler:
            handler.write(img_data)
    cont = json.loads(r.text)
    news = []
    for i in cont:
        if 'tag' in i['id']:
            url = i['id'][4:]
        else:
            url = i['id']
        news.append([i['title'], url])
    return news


if __name__ == '__main__':
    pprint(get_news('MOEX', 'SBER', 'sberbank'))