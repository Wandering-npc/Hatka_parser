import json
import random
import time
import os
import telegram

import undetected_chromedriver as uc  # pip install undetected-chromedriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
BOT = telegram.Bot(token=TELEGRAM_TOKEN)

class AvitoParse:
    """
    """

    def __init__(self, url: str, version_main=None):
        self.url = url
        self.version_main = version_main
        self.data = []

    def __set_up(self):
        options = Options()
        options.add_argument('--headless')
        self.driver = uc.Chrome(version_main=self.version_main)
        # self.driver = uc.Chrome(version_main=self.version_main, options=options)

    def __get_url(self):
        self.driver.get(self.url)

    def __parse_page(self, count):
        """Парсит открытую страницу"""
        try:
            titles = self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='item']")
            print(f'Итерация номер {count}')
            for title in titles:
                name = title.find_element(By.CSS_SELECTOR, "[itemprop='name']").text
                description = title.find_element(By.CSS_SELECTOR, "[class*='item-description']").text
                url = title.find_element(By.CSS_SELECTOR, "[data-marker='item-title']").get_attribute("href")
                price = title.find_element(By.CSS_SELECTOR, "[itemprop='price']").get_attribute("content")
                data = {
                    'хатка': name,
                    'описание': description,
                    'ссылка': url,
                    'цена': price
                }
                # if data not in self.data:
                if (int(price) <= 11000 and data not in self.data) and 'saransk'.lower() in url.lower():
                    self.data.append(data)
                    # print(data)
                    if count > 1:
                        self.__send_message(BOT, message = f'Новая хатка {data}')
                        # print(self.data[-1])               
            # self.__save_data(count)
            self.driver.quit()
            
        except Exception:
            print('че то не так в самом парсере')


    def __save_data(self, count):
        """Сохраняет результат в файл items.json"""
        with open(f"items{count}.json", 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
            # json.dump(self.data, f, ensure_ascii=False, indent=4)

    def __send_message(self, bot, message):
        """Отправка сообщения."""
        bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=message,
            )

    def parse(self):
        count = 1
        while True:
            try:
                self.__set_up()
                self.__get_url()
                self.__parse_page(count)
            except Exception:
                print('поломалось')
            finally:
                time.sleep(random.uniform(4*60, 6*60))
                count += 1


if __name__ == "__main__":
    AvitoParse(
        url='https://www.avito.ru/saransk/kvartiry/sdam/na_dlitelnyy_srok/do-20-tis-rubley-ASgBAgECAkSSA8gQ8AeQUgFFxpoMFXsiZnJvbSI6MCwidG8iOjIwMDAwfQ?f=ASgBAQECAkSSA8gQ8AeQUgFAzAgkjlmMWQFFxpoMFXsiZnJvbSI6MCwidG8iOjIwMDAwfQ&s=1',
        version_main=119,
    ).parse()