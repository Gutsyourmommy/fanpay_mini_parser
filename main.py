import requests
from bs4 import BeautifulSoup
import sqlite3

connection = sqlite3.connect('funpay.db')
cursor = connection.cursor()


FUNPAY_FORTNITE_DONATIONS = 'https://funpay.com/lots/1208/'


def get_soup(page_url: str) -> BeautifulSoup:
    html = requests.get(page_url).text
    return BeautifulSoup(html, 'html.parser')


def funpay_data_in_sql3(reference):
    increase = 0
    soup = get_soup(reference)
    main = soup.find('div', class_='tc table-hover table-clickable tc-short showcase-table tc-lazyload tc-sortable')
    food = main.find_all('a', class_='tc-item')
    for i in food:
        increase = increase + 1
        food_title = i.find('div', class_='tc-desc-text').get_text(strip=True)
        food_price = i.find('div', class_='tc-price').get_text(strip=True)
        platform = i.find('div', class_='tc-server hidden-xs').get_text(strip=True)
        seller_name = i.find('div', class_='media-user-name').get_text(strip=True)
        links = i.get('href')
        print(f'''
        Platform: {platform}
        Title: {food_title}
        Seller: {seller_name}
        Price: {food_price}
        Sequence number: {increase}
        Link: {links} 
''')
        cursor.execute('''INSERT INTO funpay_sql3_data
         (platform, title, seller, price, sequence_number, link) VALUES (?,?,?,?,?,?)''',
                       (platform, food_title, seller_name, food_price, increase, links))


funpay_data_in_sql3(FUNPAY_FORTNITE_DONATIONS)






























