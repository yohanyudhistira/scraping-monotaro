import grequests
from bs4 import BeautifulSoup
import pandas as pd

tisu_list = []


def get_urls():
    urls = []
    for x in range(1, 6):
        urls.append(f'https://www.monotaro.id/c25/c2509.html?p={x}')
    return urls


def get_data(urls):
    reqs = [grequests.get(link) for link in urls]
    resp = grequests.map(reqs)
    return resp


def parse_data(resp):
    for r in resp:
        soup = BeautifulSoup(r.content, 'html.parser')
        products = soup.find_all('li', {'class': 'item product product-item'})
        for items in products:
            name = items.find('a', {'class': 'product-item-link'}).text.strip()
            try:
                stock = items.find('div', {'class': 'product__info-status'}).text.strip()
            except:
                stock = 'Out of stock'
            start_price = items.find('span', {'class': 'price'}).text.strip()
            try:
                rating = items.find('div', {'class': 'rating-result'}).text.strip()
            except:
                rating = 'No rating'
            tisu = {
                'name': name,
                'stock': stock,
                'start price': start_price,
                'rating': rating
            }
            tisu_list.append(tisu)
    return tisu_list


urls = get_urls()
resp = get_data(urls)
df = pd.DataFrame(parse_data(resp))
print(df.head())
df.to_csv('tisu.csv', index=False)
