from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

# START BY ADDING THE SHOPEE SELLER PAGE LINK HERE
URL = 'https://shopee.ph/sayan_bmn'
# START BY ADDING THE SHOPEE SELLER PAGE LINK HERE ^^^^^^^^^^^^^^

options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--headless=new") # it's more scalable to work in headless mode 
# normally, selenium waits for all resources to download 
# we don't need it as the page also populated with the running javascript code. 
options.page_load_strategy = 'none' 
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(options=options, service=service) 
driver.maximize_window()
driver.implicitly_wait(5)
driver.get(URL)
time.sleep(10)

html = driver.find_element(By.TAG_NAME, 'body')
right_button = driver.find_element(By.CSS_SELECTOR, "button[class*='shopee-icon-button--right']")
content = driver.find_element(By.CSS_SELECTOR, "div[class*='shop-search-result-view']")

page_value = 2
mode = True
data =[]

WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'All Products')]"))).click()

def get_items():
    global page_value, mode, data
    scroll = 0
    products = content.find_elements(By.CSS_SELECTOR, "div[class*='shop-search-result-view__item']")
    WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class*='shop-search-result-view__item']")))
    while scroll < 3:
        time.sleep(3)
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(3)
        scroll += 1  

    for product in products:
            extracted_data = extract_data(product)
            data.append(extracted_data)
            
    try:
        button_name = driver.find_element(By.XPATH,f'//button[text()="{page_value}"]')
        button_name.click()
    except NoSuchElementException:
        mode = False
    else:
        page_value+=1

# function that stores the results in a list
def extract_data(products):
    name = products.find_element(By.CSS_SELECTOR,"div[class*='+ANuoG']").text
    price = products.find_element(By.CSS_SELECTOR,"span[class*='Hftxcn']").text
    sold = products.find_element(By.CSS_SELECTOR,"div[class*='YSpAGT']").text
    img = products.find_element(By.CSS_SELECTOR, "div[class*='c7e5wn']>img").get_attribute('src')
    item_link = products.find_element(By.TAG_NAME, "a").get_attribute('href')
    return {
        "price": price, 
		"name": name,
        'sold': sold,
        'img' : img,
        'link' : item_link,
    }
    
while mode:
    get_items()

# convert to a DataFrame by using Pandas and save it into a csv file
df = pd.DataFrame(data) 
df.to_csv("result.csv", index=False)
time.sleep(30)