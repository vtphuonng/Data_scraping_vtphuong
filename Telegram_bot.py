import datetime, os
import telebot 
from telegram import ParseMode
import prettytable as pt 
from selenium import webdriver
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException

# Hàm dùng để scraping
class scraping:
    def __init__(self) -> None:
        pass
    def searching_product_contain(self,find_tag,url,class_path,list_path,exp=False):
        raw_scraped = []
        url = url
        driver = webdriver.Edge()
        driver.get(url)
        time.sleep(5)
        display = Display(visible=0, size=(800, 600))
        display.start()
        y = 1080
        for i in range(2):
            driver.execute_script(f"window.scrollTo(0, {y})")
            y += 700 
            time.sleep(3)
        if find_tag != False:
            for tr in driver.find_elements(By.XPATH, class_path):
                l1 = []
                tds = tr.find_elements(By.TAG_NAME, list_path[0])
                for i in tds:
                    l1.append(i.text)
                raw_scraped.append(l1)
        else:
            print('error')
        return self.to_csv(raw_scraped)
    @staticmethod
    def to_csv(main):
        raw_df = pd.DataFrame(main)
        f_list = []
        for i in raw_df:
            name = []
            for item in raw_df[i]:
                str1 = ''
                try:
                    str1 = item.text
                except Exception as e:
                    str1 = item
                name.append(str1)
            f_list.append(name)
        new_raw = pd.DataFrame(f_list)
        new_raw = new_raw.T
        print(new_raw)
        new_raw.to_csv('data.csv')
        return "Success"

#tạo 1 hàm để render table 
def render_talbe():
    _today = (datetime.datetime.now()).strftime("%Y%m%d") 
    file = os.path.join("data", f"{_today}.csv") 
    with open(file, "r", encoding='utf-8') as f: 
        result  = f.readlines() 
        result.pop(0) 
    table = pt.PrettyTable(['Date', 'MD5', 'Ip', 'Tools']) 
    table.title = "Thông Tin Mới" 
    for row_ in result:
        row = row_.replace("\n", "").split(",")
        table.add_row([row[0], row[1], row[2], row[3]])
    return table


if __name__ == "__main__": 
    bot = telebot.TeleBot('Telegram API')
    list_path = ["td"]
    url = 'http://vxvault.net/ViriList.php'
    try:
        @bot.message_handler(func=lambda message: True,commands=["news"]) 
        def news(message):
            main = scraping.searching_product_contain(True, url,\
                                '''//div[@id='container']/div[@id='page']/table/tbody/tr''',\
                                list_path,\
                               )
            table = render_talbe()
            bot.reply_to(message, f"<pre>{table}</pre>", parse_mode=ParseMode.HTML) 
            bot.reply_to('Hello there')
    except Exception as e:
            print(e)
    finally:
        bot.polling()