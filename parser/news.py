import requests
from bs4 import BeautifulSoup

URL = 'https://www.securitylab.ru/news/'

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
}


def get_html(url, params=''):
    req = requests.get(url, headers=HEADERS, params=params)
    return req


def get_data(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all('a', class_='article-card inline-card')
    news = []
    for item in items:
        news.append({
            'time': item.find("time").getText(),
            'title': item.find("h2", class_='article-card-title').getText(),
            'desc': item.find("p").getText(),
            'link': "https://www.securitylab.ru/" + item.get('href'),
            # 'photo': "https://www.securitylab.ru" + item.find('div', class_='article-img').find('img').get('src')
        })
    return news


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        news = []
        for page in range(1, 2):
            html = get_html(f"{URL}page1_{page}.php")
            news.extend(get_data(html.text))
        # print(news)
        return news
    else:
        raise Exception("ERROR in parser!")
