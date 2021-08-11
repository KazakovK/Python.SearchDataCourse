from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import ast

client = MongoClient('localhost', 27017)
db = client['goods_database']
goods_db = db.goods

chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-notifications")  # Убираем подписку на уведомления

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get("https://www.mvideo.ru/")

button_loction = driver.find_element_by_class_name('geolocation__action-approve-city')
button_loction.click()  # Выбираем предложенный город

# Проходим по всей странице для прогрузки данных
element = driver.find_element_by_class_name('footer-copyright')
actions = ActionChains(driver)
actions.move_to_element(element).perform()

# Идем в новинки
news_goods = driver.find_element_by_xpath("//div[contains(h2,'Новинки')]")
actions.move_to_element(news_goods).perform()
goods_dict = []
while True:
    try:
        button_wait = WebDriverWait(driver, 10)
        button_click = button_wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                     '//div[contains(h2,"Новинки")]/../..//a[contains(@class,"next-btn")]')))
        news_goods = driver.find_elements_by_xpath(
            '//div[contains(h2,"Новинки")]/../..//a[contains(@class,"fl-product-tile-picture")]')

        button_click.click()
    except Exception as e:
        break

for good in news_goods:
    goods = {}
    new_good = good.get_attribute('data-product-info')
    new_good = ast.literal_eval(new_good)
    goods_db.update_one({'productId': new_good['productId']},
                        {'$set': new_good},
                        upsert=True)

    print(new_good)
