import bs4
import time
import csv
from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

count = 1
while count <= 149:
    with webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options) as driver:  # Открываем хром
        driver.get(f"https://lis-skins.ru/market/csgo/?page={count}")  # Открываем страницу
        time.sleep(3)  # Время на прогрузку страницы
        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        heads = soup.find('div', class_='skins-market-skins-list').find_all('a', href=True)
        print(len(heads))
        for head in heads:
            print(head['href'])
            url = (head['href'])
            with webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=chrome_options) as driver:  # Открываем хром
                driver.get(url)  # Открываем страницу
                time.sleep(2)  # Время на прогрузку страницы
                block = bs4.BeautifulSoup(driver.page_source, 'html.parser')
                name = block.find('div', class_='skin-name')
                try:
                    print(name.text.strip())
                    zagol = (name.text.strip())
                except:
                    print('No name')
                    zagol = 'No name'
                min_price = block.find('div', class_='min-price-value')
                print(' '.join(min_price.text.strip().split()))
                new_price = (' '.join(min_price.text.strip().split()))
                params = block.find('div', class_='specs-list').find_all('div', class_='spec-item')
                print(': '.join(params[0].text.strip().split()))
                param_1 = (': '.join(params[0].text.strip().split()))
                print(': '.join(params[1].text.strip().split()))
                param_2 = (': '.join(params[1].text.strip().split()))
                try:
                    print(': '.join(params[2].text.strip().split()))
                    param_3 = (': '.join(params[2].text.strip().split()))
                except:
                    print('None')
                    param_3 = 'None'
                pix = block.find('div', class_='image-block').find('a', href=True)
                print(pix['href'])
                photo = (pix['href'])
                print('\n')

                storage = {'name': zagol, 'min_price': new_price, 'param_1': param_1, 'param_2': param_2,
                           'param_3': param_3, 'photo': photo, 'URL': url}
                fields = ['Name', 'Min_Price', 'Param_1', 'Param_2', 'Param_3', 'Photo', 'URL']
                with open('skins.csv', 'a+', encoding='utf-16') as file:
                    pisar = csv.writer(file, delimiter=';', lineterminator='\r')

                    # Проверяем, находится ли файл в начале и пуст ли
                    file.seek(0)
                    if len(file.read()) == 0:
                        pisar.writerow(fields)  # Записываем заголовки, только если файл пуст

                    pisar.writerow(
                        [storage['name'], storage['min_price'], storage['param_1'], storage['param_2'],
                         storage['param_3'],
                         storage['photo'], storage['URL']])
        count += 1
        print(count)
