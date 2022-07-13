from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as BS
import json, csv
import time

def get_html(ua, path, url):
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={ua}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.binary_location = 'C:\Program Files\Google\Chrome Beta\Application\chrome.exe'

    service = Service(path)
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.maximize_window()
        driver.get(url)
        time.sleep(5)

        last_height = 2500
        current_height = 0
        while current_height < last_height:
            driver.execute_script(f'window.scrollBy(0, {current_height});')

            print(current_height, last_height)
            time.sleep(5)
            current_height += 250

        time.sleep(5)

        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)
    finally:
        driver.stop_client()
        driver.close()
        driver.quit()

def get_data(url):
    data = []

    with open('index.html', encoding='utf-8') as file:
        html = file.read()

    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'name', 'symbol', 'logo', 'price', 'market_cap', 'href'
        ])

    soup = BS(html, 'lxml')

    all_cryptos = soup.find(class_='h7vnx2-2 czTsgW cmc-table').find('tbody').find_all('tr')

    count = 1
    for crypto in all_cryptos:
        name = crypto.find(class_='sc-16r8icm-0 sc-1teo54s-1 dNOTPP').find('p').text
        href = url + crypto.find(class_='sc-16r8icm-0 escjiH').find(class_='cmc-link').get('href')
        symbol = crypto.find(class_='sc-1teo54s-2 fZIJcI').find('p').text
        logo = crypto.find(class_='sc-16r8icm-0 sc-1teo54s-0 dBKWCw').find('img').get('src')
        market_cap = crypto.find('span', class_='sc-1ow4cwt-1 ieFnWP').text
        price = crypto.find(class_='sc-131di3y-0 cLgOOr').find('a').text

        data.append(
            {
                'name': name,
                'symbol': symbol,
                'logo': logo,
                'price': price,
                'market_cap': market_cap,
                'href': href
            }
        )

        with open('data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, symbol, logo, price, market_cap, href])

        print(count)
        count += 1

    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    ua = UserAgent().random
    path = r'C:\Users\name\Documents\GitHub\chromedriver.exe'
    url = 'https://coinmarketcap.com/'

    get_html(ua, path, url)
    get_data(url)

if __name__ == '__main__':
    main()